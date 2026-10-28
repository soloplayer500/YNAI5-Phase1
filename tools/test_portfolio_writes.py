"""Offline regression tests: python -m unittest discover -s tools -p 'test_portfolio_writes.py' -v

Requires PyYAML for workflow contract checks. No service credentials or API calls.
Git integration tests simulate the lock boundary; GitHub enforces the actual queue.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'tools/push-portfolio.py'
STATE = 'projects/crypto-monitoring/kraken/predictions.json'
CACHE = 'projects/crypto-monitoring/kraken/.cache.json'


def git(cwd, *args, check=True):
    return subprocess.run(['git', *args], cwd=cwd, check=check,
                          capture_output=True, text=True)


class PortfolioWrites(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.remote = self.root / 'remote.git'
        git(self.root, 'init', '--bare', '--initial-branch=master', str(self.remote))
        self.a = self.clone('a')
        self.commit(self.a, STATE, '[]\n')
        self.commit(self.a, CACHE, '{}\n')
        git(self.a, 'push', '-u', 'origin', 'master')
        self.b = self.clone('b')

    def clone(self, name):
        path = self.root / name
        git(self.root, 'clone', str(self.remote), str(path))
        git(path, 'config', 'user.name', 'Regression Bot')
        git(path, 'config', 'user.email', 'test@example.invalid')
        return path

    def commit(self, repo, path, content):
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        git(repo, 'add', path)
        git(repo, 'commit', '-m', 'test update')
        return git(repo, 'rev-parse', 'HEAD').stdout.strip()

    def push(self, repo, ref='refs/heads/master'):
        return subprocess.run([sys.executable, str(HELPER)], cwd=repo,
                              env={**os.environ, 'GITHUB_REF': ref},
                              capture_output=True, text=True)

    def remote_content(self, path):
        return git(self.remote, 'show', f'master:{path}').stdout

    def test_workflow_contract(self):
        for name in ('portfolio-sync', 'morning-briefing'):
            config = yaml.safe_load((ROOT / '.github/workflows' / f'{name}.yml').read_text())
            self.assertEqual(config['concurrency'], {
                'group': 'portfolio-state-${{ github.ref }}',
                'cancel-in-progress': False, 'queue': 'max'})
            # PyYAML's YAML 1.1 loader parses 'on' as True.
            triggers = config.get('on', config.get(True))
            self.assertEqual(triggers['schedule'], [{'cron': '0 13 * * *'}])
            self.assertIn('workflow_dispatch', triggers)
            steps = next(iter(config['jobs'].values()))['steps']
            self.assertEqual(steps[0]['with']['ref'], '${{ github.ref }}')
            self.assertEqual(steps[0]['with']['fetch-depth'], 0)
            self.assertIn('python tools/push-portfolio.py', steps[-1]['run'])

    def test_serialized_runs_in_either_order_preserve_history(self):
        for order in (('portfolio', 'briefing'), ('briefing', 'portfolio')):
            with self.subTest(order=order):
                # Both events can reference the same old SHA, but the queued
                # checkout must resolve the branch only after the first push.
                git(self.a, 'pull', '--ff-only')
                current = json.loads((self.a / STATE).read_text())
                first = self.commit(self.a, STATE, json.dumps(current + [order[0]]))
                self.assertEqual(self.push(self.a).returncode, 0)
                git(self.b, 'fetch', 'origin', 'master')
                git(self.b, 'checkout', '-B', 'master', 'origin/master')
                self.assertEqual(git(self.b, 'rev-parse', 'HEAD').stdout.strip(), first)
                current = json.loads((self.b / STATE).read_text())
                self.commit(self.b, STATE, json.dumps(current + [order[1]]))
                self.assertEqual(self.push(self.b).returncode, 0)
                self.assertEqual(json.loads(self.remote_content(STATE))[-2:], list(order))
                self.assertEqual(git(self.remote, 'merge-base', '--is-ancestor', first, 'master').returncode, 0)

    def test_disjoint_remote_commit_preserved_with_dirty_cache(self):
        local = self.commit(self.a, STATE, '["local"]\n')
        (self.a / CACHE).write_text('{"unstaged": true}\n')
        remote = self.commit(self.b, 'daily-output.txt', 'daily task\n')
        git(self.b, 'push')
        result = self.push(self.a)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.remote_content(STATE), '["local"]\n')
        self.assertEqual(self.remote_content('daily-output.txt'), 'daily task\n')
        self.assertEqual((self.a / CACHE).read_text(), '{"unstaged": true}\n')
        for sha in (local, remote):
            git(self.remote, 'merge-base', '--is-ancestor', sha, 'master')

    def test_competing_snapshot_refused_and_local_commit_retained(self):
        local = self.commit(self.a, STATE, '["local"]\n')
        self.commit(self.b, STATE, '["remote"]\n')
        git(self.b, 'push')
        result = self.push(self.a)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('refusing to overwrite', result.stderr)
        self.assertEqual(self.remote_content(STATE), '["remote"]\n')
        self.assertEqual(git(self.a, 'rev-parse', 'HEAD').stdout.strip(), local)

    def test_other_snapshot_state_also_refused(self):
        self.commit(self.a, STATE, '["local"]\n')
        self.commit(self.b, 'projects/crypto-monitoring/kraken/.alert-state.json', '{"sent": true}')
        git(self.b, 'push')
        result = self.push(self.a)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('refusing to overwrite', result.stderr)
        self.assertEqual(self.remote_content(STATE), '[]\n')

    def test_no_changes(self):
        before = git(self.remote, 'rev-parse', 'master').stdout
        self.assertEqual(self.push(self.a).returncode, 0)
        self.assertEqual(git(self.remote, 'rev-parse', 'master').stdout, before)

    def test_non_branch_ref_refused(self):
        self.assertNotEqual(self.push(self.a, 'refs/tags/test').returncode, 0)

    def test_permanent_rejection_does_not_loop(self):
        self.commit(self.a, STATE, '["local"]\n')
        hook = self.remote / 'hooks/pre-receive'
        hook.write_text('#!/bin/sh\necho rejected >> "$GIT_DIR/rejections"\nexit 1\n')
        hook.chmod(0o755)
        self.assertNotEqual(self.push(self.a).returncode, 0)
        self.assertEqual((self.remote / 'rejections').read_text().count('rejected'), 1)

    def test_repeated_remote_advancement_is_bounded(self):
        self.commit(self.a, STATE, '["local"]\n')
        hook = self.a / '.git/hooks/pre-push'
        # Each push races with another disjoint writer. No real network involved.
        hook.write_text(f'''#!/bin/sh
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
cd '{self.b}' || exit 1
echo next >> race.txt
git add race.txt
git commit -m race >/dev/null
git push origin master >/dev/null 2>&1
''')
        hook.chmod(0o755)
        result = self.push(self.a)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('at most 3 attempts', result.stderr)
        self.assertEqual(self.remote_content('race.txt').count('next'), 3)
        self.assertEqual(self.remote_content(STATE), '[]\n')
        self.assertEqual((self.a / STATE).read_text(), '["local"]\n')


if __name__ == '__main__':
    unittest.main()
