// dashboard.js — YNAI5 Control Center v1.0
// Single polling file. No modules. Drives all UI from /api/status + /api/ynai5logs.

'use strict';

// ── Config ──────────────────────────────────────────────────────────────────
const POLL_STATUS_MS  = 8_000;
const POLL_LOGS_MS    = 15_000;
const MAX_TASKS_SHOWN = 5;
const MAX_LOGS_SHOWN  = 5;

// Static agent definitions — state is derived from heartbeat at runtime
const AGENTS = [
  { id: 'conductor', name: 'Conductor', model: 'Claude',      icon: '🧠', avatarClass: '',        role: 'Coordinating agents',  badges: [{label:'Control', cls:''}] },
  { id: 'scout',     name: 'Scout',     model: 'Gemini',      icon: '📚', avatarClass: 'scout',   role: 'Researching sources',  badges: [{label:'Research', cls:'blue'}] },
  { id: 'director',  name: 'Director',  model: 'Claude',      icon: '✍️', avatarClass: 'director', role: 'Writing content',     badges: [{label:'Content', cls:''}] },
  { id: 'pulse',     name: 'Pulse',     model: 'Monitor',     icon: '📡', avatarClass: 'pulse',   role: 'Monitoring system',    badges: [{label:'Monitor', cls:'red'}] },
  { id: 'forge',     name: 'Forge',     model: 'Claude Code', icon: '🛠️', avatarClass: 'forge',   role: 'Building interface',   badges: [{label:'Build', cls:'yellow'}] },
  { id: 'shadow',    name: 'Shadow',    model: 'Sim only',    icon: '📈', avatarClass: 'shadow',  role: 'Paper trading',        badges: [{label:'Sim', cls:'green'}] },
  { id: 'echo',      name: 'Echo',      model: 'Ollama',      icon: '💬', avatarClass: 'echo',    role: 'Fast replies',         badges: [{label:'Local', cls:'blue'}] },
];

// Maps heartbeat active_agent value → agent card id
const AGENT_MAP = { claude: 'conductor', gemini: 'scout' };

// ── State ────────────────────────────────────────────────────────────────────
let lastHeartbeat = null;

// ── Init ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  renderAgentGrid();
  pollStatus();
  pollLogs();
  setInterval(pollStatus, POLL_STATUS_MS);
  setInterval(pollLogs,   POLL_LOGS_MS);
  initCommandBar();
});

// ── Polling ──────────────────────────────────────────────────────────────────
async function pollStatus() {
  try {
    const res  = await fetch('/api/status?t=' + Date.now());
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();

    const hb       = data.heartbeat  || {};
    const vm       = data.vm         || {};
    const services = data.services   || {};
    const drive    = data.drive_mounted;

    lastHeartbeat = hb;

    updateHeader(hb);
    updateOrchestrator(hb);
    updateTasks(hb.task_queue || []);
    updateHealth(vm, services, drive);
    updateAgentCards(hb);
    updateRefreshTime();

  } catch (e) {
    setStatusOffline('VM unreachable');
    console.warn('[dashboard] status poll failed:', e.message);
  }
}

async function pollLogs() {
  try {
    const res  = await fetch('/api/ynai5logs?last=10&t=' + Date.now());
    if (!res.ok) return;
    const data = await res.json();
    updateLogs(data.events || []);
  } catch (e) {
    // silent — logs are secondary
  }
}

// ── Header ───────────────────────────────────────────────────────────────────
function updateHeader(hb) {
  const dot  = document.getElementById('status-dot');
  const txt  = document.getElementById('status-text');
  const chip = document.getElementById('hero-chip');

  if (!hb || hb.error) {
    setStatusOffline(hb?.error || 'offline');
    return;
  }

  const isWorking = hb.status === 'working';
  dot.className   = 'dot' + (isWorking ? ' working' : '');
  txt.textContent = isWorking
    ? 'Working · ' + (hb.active_agent || 'agent') + ' active'
    : 'Live · idle';

  if (chip) {
    const done = hb.stats?.tasks_completed || 0;
    chip.textContent = done + ' tasks completed';
  }
}

function setStatusOffline(msg) {
  const dot = document.getElementById('status-dot');
  const txt = document.getElementById('status-text');
  if (dot) dot.className = 'dot offline';
  if (txt) txt.textContent = msg;
}

function updateRefreshTime() {
  const el = document.getElementById('refresh-time');
  if (el) el.textContent = new Date().toLocaleTimeString('en-US', {hour:'2-digit', minute:'2-digit', second:'2-digit'});
}

// ── Orchestrator panel ────────────────────────────────────────────────────────
function updateOrchestrator(hb) {
  const status    = hb.status || 'unknown';
  const active    = hb.active_agent || '—';
  const completed = hb.stats?.tasks_completed ?? '—';

  setText('orch-status',    status);
  setText('orch-active',    active);
  setText('orch-completed', String(completed));
}

// ── Task list ─────────────────────────────────────────────────────────────────
function updateTasks(queue) {
  const el = document.getElementById('task-list');
  if (!el) return;

  if (!queue.length) {
    el.innerHTML = '<div class="item empty">No tasks queued</div>';
    return;
  }

  el.innerHTML = queue.slice(0, MAX_TASKS_SHOWN).map(t => {
    const label = t.command ? t.command.slice(0, 60) : (t.type || 'task');
    const agent = t.assigned_to ? ' → ' + t.assigned_to : '';
    return '<div class="item">' + escHtml(label + agent) + '</div>';
  }).join('');

  if (queue.length > MAX_TASKS_SHOWN) {
    el.innerHTML += '<div class="item empty">+' + (queue.length - MAX_TASKS_SHOWN) + ' more</div>';
  }
}

// ── Log list ──────────────────────────────────────────────────────────────────
function updateLogs(events) {
  const el = document.getElementById('log-list');
  if (!el) return;

  if (!events.length) {
    el.innerHTML = '<div class="item empty">No events yet</div>';
    return;
  }

  // Most recent first
  const recent = [...events].reverse().slice(0, MAX_LOGS_SHOWN);
  el.innerHTML = recent.map(ev => {
    const component = ev.component || 'system';
    const issue     = ev.issue     || ev.fix || ev.root_cause || '';
    const text      = component + ': ' + issue.slice(0, 60);
    return '<div class="item">' + escHtml(text) + '</div>';
  }).join('');
}

// ── Health panel ──────────────────────────────────────────────────────────────
function updateHealth(vm, services, drive) {
  if (vm.cpu_percent  != null) setText('h-cpu',    vm.cpu_percent + '%');
  if (vm.ram_percent  != null) setText('h-ram',    vm.ram_percent + '% (' + vm.ram_used_gb + 'GB)');
  if (vm.disk_percent != null) setText('h-disk',   vm.disk_percent + '%');
  if (vm.uptime_hours != null) setText('h-uptime', vm.uptime_hours + 'h');

  const total  = Object.keys(services).length;
  const online = Object.values(services).filter(s => s === 'active').length;
  if (total) setText('h-services', online + '/' + total + ' active');

  setText('h-drive', drive ? 'mounted' : 'not mounted');
}

// ── Agent cards ───────────────────────────────────────────────────────────────
function renderAgentGrid() {
  const grid = document.getElementById('agent-grid');
  if (!grid) return;

  grid.innerHTML = AGENTS.map(a => {
    const isConductor = a.id === 'conductor';
    const badges      = a.badges.map(b =>
      '<span class="badge ' + b.cls + '">' + b.label + '</span>'
    ).join('');

    return `
      <div class="card ${isConductor ? 'conductor-card' : ''}" id="card-${a.id}">
        <div class="card-head">
          <span class="card-name">${a.name}</span>
          <span class="card-model">${a.model}</span>
        </div>
        <div class="card-body">
          <div class="card-activity">
            <div class="avatar ${a.avatarClass}">${a.icon}</div>
            <div>
              <div class="card-state" id="state-label-${a.id}">${a.role}</div>
              <div class="card-state" id="state-val-${a.id}">State: idle</div>
            </div>
          </div>
          <div class="card-task" id="task-${a.id}">—</div>
          <div class="pills">${badges}<span class="badge muted" id="badge-state-${a.id}">Idle</span></div>
        </div>
      </div>`;
  }).join('');
}

function updateAgentCards(hb) {
  const activeCard = AGENT_MAP[hb.active_agent] || null;
  const queue      = hb.task_queue     || [];
  const last       = hb.last_task_result || {};
  const status     = hb.status         || 'idle';

  AGENTS.forEach(a => {
    let state = 'idle';
    let task  = '—';

    if (a.id === activeCard) {
      state = 'working';
      task  = last.result
        ? last.result.slice(0, 80)
        : 'executing task...';
    } else if (a.id === 'conductor' && queue.length > 0) {
      state = 'routing';
      task  = 'routing ' + queue.length + ' task(s)';
    } else if (a.id === 'conductor' && status === 'working') {
      state = 'active';
      task  = 'supervising agent';
    } else if (a.id === 'pulse') {
      state = 'watching';
      task  = 'health + alerts';
    }

    // Update DOM
    const stateEl = document.getElementById('state-val-' + a.id);
    const taskEl  = document.getElementById('task-' + a.id);
    const badgeEl = document.getElementById('badge-state-' + a.id);

    if (stateEl) {
      stateEl.className = 'card-state state-' + state;
      stateEl.textContent = 'State: ' + state;
    }
    if (taskEl)  taskEl.textContent  = task;
    if (badgeEl) {
      badgeEl.textContent = capitalize(state);
      badgeEl.className   = 'badge ' + stateBadgeClass(state);
    }
  });
}

// ── Command bar ───────────────────────────────────────────────────────────────
function initCommandBar() {
  const input     = document.getElementById('cmd-input');
  const sendBtn   = document.getElementById('cmd-send');
  const routeChip = document.getElementById('route-indicator');

  if (!input || !sendBtn) return;

  // Update route chip as user types
  input.addEventListener('input', () => {
    const val = input.value.trim();
    const toClaude = val.startsWith('@claude');
    if (routeChip) routeChip.textContent = toClaude ? '→ claude' : '→ gemini';
  });

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendCommand();
    }
  });

  sendBtn.addEventListener('click', sendCommand);
}

async function sendCommand() {
  const input   = document.getElementById('cmd-input');
  const sendBtn = document.getElementById('cmd-send');
  if (!input || !input.value.trim()) return;

  let raw        = input.value.trim();
  let assignedTo = 'gemini';
  let command    = raw;

  if (raw.startsWith('@claude')) {
    assignedTo = 'claude';
    command    = raw.replace(/^@claude\s*/i, '').trim() || raw;
  } else if (raw.startsWith('@gemini')) {
    command = raw.replace(/^@gemini\s*/i, '').trim() || raw;
  }

  sendBtn.disabled = true;
  input.value      = '';
  if (document.getElementById('route-indicator'))
    document.getElementById('route-indicator').textContent = '→ gemini';

  // Optimistic: add task to left panel immediately
  addOptimisticTask(command, assignedTo);

  try {
    const res = await fetch('/api/task', {
      method:  'POST',
      headers: {'Content-Type': 'application/json'},
      body:    JSON.stringify({command, assigned_to: assignedTo, priority: 1, context: ''}),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      console.warn('[dashboard] task send failed:', err);
    } else {
      // Refresh status immediately after queuing
      pollStatus();
    }
  } catch (e) {
    console.warn('[dashboard] task send error:', e.message);
  } finally {
    sendBtn.disabled = false;
  }
}

function addOptimisticTask(command, assignedTo) {
  const el = document.getElementById('task-list');
  if (!el) return;
  const emptyEl = el.querySelector('.item.empty');
  if (emptyEl) emptyEl.remove();

  const item = document.createElement('div');
  item.className   = 'item';
  item.textContent = command.slice(0, 60) + ' → ' + assignedTo;
  el.insertBefore(item, el.firstChild);

  // Cap at MAX_TASKS_SHOWN
  const items = el.querySelectorAll('.item:not(.empty)');
  if (items.length > MAX_TASKS_SHOWN) items[items.length - 1].remove();
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function escHtml(str) {
  return String(str)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}

function capitalize(str) {
  return str ? str.charAt(0).toUpperCase() + str.slice(1) : str;
}

function stateBadgeClass(state) {
  const map = {
    working:  'yellow',
    active:   'green',
    routing:  '',       // purple (default)
    watching: 'blue',
    idle:     'muted',
    blocked:  'red',
  };
  return map[state] || 'muted';
}
