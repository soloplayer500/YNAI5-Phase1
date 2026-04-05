#!/bin/bash
# ============================================================
# YNAI5-Phase1 VM Bootstrap Script
# Run this once on the GCP VM after SSH-ing in.
# Usage: bash vm-bootstrap.sh
# ============================================================

set -e
RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'
log() { echo -e "${CYAN}[YNAI5]${NC} $1"; }
ok()  { echo -e "${GREEN}[OK]${NC} $1"; }
err() { echo -e "${RED}[ERR]${NC} $1"; }

log "YNAI5-Phase1 VM Bootstrap starting..."
echo ""

# ── 1. System packages ──────────────────────────────────────
log "Installing system packages..."
sudo apt update -qq && sudo apt upgrade -y -qq
sudo apt install -y -qq python3-pip python3-venv git curl wget unzip tmux htop nginx fuse3
ok "System packages installed"

# ── 2. Node.js 20 LTS ──────────────────────────────────────
log "Installing Node.js 20 LTS..."
if ! node --version 2>/dev/null | grep -q "v20"; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - -q
  sudo apt install -y -qq nodejs
fi
ok "Node.js $(node --version) installed"

# ── 3. Gemini CLI ────────────────────────────────────────────
log "Installing Gemini CLI..."
sudo npm install -g @google/gemini-cli --quiet 2>&1 | tail -1
ok "Gemini CLI installed: $(gemini --version 2>/dev/null || echo 'check manually')"

# ── 4. Claude Code ───────────────────────────────────────────
log "Installing Claude Code..."
sudo npm install -g @anthropic-ai/claude-code --quiet 2>&1 | tail -1
ok "Claude Code installed: $(claude --version 2>/dev/null || echo 'check manually')"

# ── 5. Python packages ───────────────────────────────────────
log "Installing Python packages..."
pip3 install -q google-generativeai fastapi uvicorn psutil requests watchdog
ok "Python packages installed"

# ── 6. rclone ────────────────────────────────────────────────
log "Installing rclone..."
if ! rclone --version &>/dev/null; then
  curl -fsSL https://rclone.org/install.sh | sudo bash -s - --quiet
fi
ok "rclone $(rclone --version | head -1) installed"

# ── 7. Create /ynai5_runtime ─────────────────────────────────
log "Creating /ynai5_runtime directory structure..."
sudo mkdir -p /ynai5_runtime/{scripts,logs,config,dashboard}
sudo chown -R $USER:$USER /ynai5_runtime
ok "/ynai5_runtime created"

# ── 8. Create Drive mount point ──────────────────────────────
log "Creating /mnt/gdrive mount point..."
sudo mkdir -p /mnt/gdrive
sudo chown $USER:$USER /mnt/gdrive
ok "/mnt/gdrive created"

# ── 9. Copy scripts from this repo ───────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
log "Copying scripts from $SCRIPT_DIR..."

cp "$SCRIPT_DIR/scripts/gemini_worker.py" /ynai5_runtime/scripts/
cp "$SCRIPT_DIR/scripts/claude_runner.py" /ynai5_runtime/scripts/
cp "$SCRIPT_DIR/dashboard/main.py" /ynai5_runtime/dashboard/
cp "$SCRIPT_DIR/dashboard/index.html" /ynai5_runtime/dashboard/
ok "Scripts copied"

# ── 10. Create .env template ─────────────────────────────────
if [ ! -f /ynai5_runtime/.env ]; then
  log "Creating .env template..."
  cat > /ynai5_runtime/.env << 'EOF'
# YNAI5-Phase1 Environment Variables
# Fill these in before starting services

GEMINI_API_KEY=
ANTHROPIC_API_KEY=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Optional
BRAVE_SEARCH_API_KEY=
KRAKEN_API_KEY=
KRAKEN_API_SECRET=
EOF
  chmod 600 /ynai5_runtime/.env
  ok ".env template created at /ynai5_runtime/.env"
  echo ""
  echo -e "${RED}ACTION REQUIRED:${NC} Edit /ynai5_runtime/.env and add your API keys"
  echo "  nano /ynai5_runtime/.env"
  echo ""
else
  ok ".env already exists — skipping"
fi

# ── 11. Install systemd services ─────────────────────────────
log "Installing systemd services..."
sudo cp "$SCRIPT_DIR/systemd/"*.service /etc/systemd/system/
sudo systemctl daemon-reload
ok "systemd services installed"

# ── 12. Configure Nginx ──────────────────────────────────────
log "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/ynai5 > /dev/null << 'NGINX'
server {
    listen 80;
    server_name _;

    # YNAI5 Dashboard
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 60s;
    }

    # Netdata system metrics
    location /metrics/ {
        proxy_pass http://127.0.0.1:19999/;
        proxy_set_header Host $host;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/ynai5 /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
ok "Nginx configured"

# ── 13. Install Netdata ──────────────────────────────────────
log "Installing Netdata..."
if ! systemctl is-active netdata &>/dev/null; then
  wget -qO /tmp/netdata-kickstart.sh https://get.netdata.cloud/kickstart.sh
  sh /tmp/netdata-kickstart.sh --stable-channel --disable-telemetry --dont-start-it 2>&1 | tail -3
  sudo systemctl enable netdata
  sudo systemctl start netdata
fi
ok "Netdata installed"

# ── 14. Configure rclone (MANUAL STEP) ──────────────────────
echo ""
echo "════════════════════════════════════════"
echo " MANUAL STEP REQUIRED: rclone OAuth"
echo "════════════════════════════════════════"
echo ""
echo "Run this on YOUR WINDOWS MACHINE first:"
echo ""
echo "  rclone config show"
echo ""
echo "Copy the [gdrive] section, then on this VM:"
echo ""
echo "  mkdir -p ~/.config/rclone"
echo "  nano ~/.config/rclone/rclone.conf"
echo ""
echo "Paste the [gdrive] config block, save, then:"
echo ""
echo "  rclone lsd gdrive:/"
echo "  (should list your Drive folders)"
echo ""
echo "Once confirmed, enable and start services:"
echo ""
echo "  sudo systemctl enable ynai5-drive ynai5-gemini ynai5-claude ynai5-dashboard"
echo "  sudo systemctl start ynai5-drive"
echo "  sleep 5"
echo "  sudo systemctl start ynai5-gemini ynai5-claude ynai5-dashboard"
echo ""
echo "Then fill in /ynai5_runtime/.env with API keys."
echo ""

# ── Summary ─────────────────────────────────────────────────
echo "════════════════════════════════════════"
echo -e "${GREEN} YNAI5-Phase1 VM Bootstrap Complete!${NC}"
echo "════════════════════════════════════════"
echo " Packages: Python ✓ | Node.js ✓ | rclone ✓"
echo " Gemini CLI: installed | Claude Code: installed"
echo " /ynai5_runtime: created"
echo " systemd services: installed (not yet started)"
echo " Nginx: configured"
echo " Netdata: installed"
echo ""
echo " Next steps:"
echo "  1. Copy rclone config from Windows"
echo "  2. Edit /ynai5_runtime/.env with API keys"
echo "  3. systemctl start ynai5-drive (then start others)"
echo "  4. Dashboard: http://$(curl -s ifconfig.me 2>/dev/null || echo 'YOUR-VM-IP')/"
echo "  5. Metrics:   http://$(curl -s ifconfig.me 2>/dev/null || echo 'YOUR-VM-IP')/metrics/"
echo ""
