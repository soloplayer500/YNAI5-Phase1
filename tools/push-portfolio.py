#!/usr/bin/env python3
"""Push an already committed snapshot; retry only disjoint remote changes.

Never regenerate data or resend notifications. Keep the local snapshot commit
on failure. The two portfolio workflows must also share a concurrency group
and check out the branch tip *after* acquiring it.
"""
import os
import subprocess


def git(*args, check=True):
    return subprocess.run(["git", *args], check=check, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def changed(base, head):
    return set(git("diff", "--name-only", "--no-renames", "-z", base, head).stdout.split("\0")) - {""}


def main():
    ref = os.environ["GITHUB_REF"]
    if not ref.startswith("refs/heads/"):
        raise RuntimeError("Snapshot writes require a branch ref")
    # Full history is required to find the common ancestor after remote advancement.
    for attempt in range(3):
        result = git("push", "origin", f"HEAD:{ref}", check=False)
        if result.returncode == 0:
            print(result.stderr)
            return
        print(result.stderr)
        if attempt == 2:
            break
        git("fetch", "--no-tags", "origin", ref)
        remote = git("rev-parse", "FETCH_HEAD").stdout.strip()
        base = git("merge-base", "HEAD", remote).stdout.strip()
        # No remote advancement: permissions/network/hooks will not be fixed by merging.
        if base == remote:
            break
        local_files = changed(base, "HEAD")
        remote_files = changed(base, remote)
        # JSON snapshots and cooldown/prediction state are not safely text-mergeable,
        # even when Git could merge different lines without a conflict.
        protected = ("projects/crypto-monitoring/kraken/",
                     "projects/crypto-monitoring/telegram-sessions/")
        if local_files & remote_files or any(p.startswith(protected) for p in remote_files):
            raise RuntimeError("Remote changed snapshot state or local output paths; refusing to overwrite. Local commit retained.")
        # Merge preserves both commits and tolerates the monitor's unstaged cache.
        # No force push, reset, stash, conflict preference, or analysis retry.
        result = git("merge", "--no-edit", remote, check=False)
        if result.returncode:
            git("merge", "--abort", check=False)
            raise RuntimeError("Could not safely merge remote changes; local commit retained.")
    raise RuntimeError("Snapshot push failed after at most 3 attempts; local commit retained.")


if __name__ == "__main__":
    main()
