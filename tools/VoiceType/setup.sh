#!/bin/bash
# VoiceType one-time setup. Run:  bash setup.sh
set -e
cd "$(dirname "$0")"

echo "== VoiceType setup =="

# 1. Python check
if ! command -v python3 &>/dev/null; then
  echo "python3 not found. Install Xcode Command Line Tools first:  xcode-select --install"
  exit 1
fi

# 2. Virtual env + dependencies
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
./.venv/bin/pip install --quiet --upgrade pip
./.venv/bin/pip install --quiet sounddevice numpy requests pynput
echo "✓ Dependencies installed"

# 3. Groq API key
if [ ! -f "config.json" ]; then
  echo ""
  echo "Get a FREE API key at: https://console.groq.com/keys  (sign up with Google, no card needed)"
  read -p "Paste your Groq API key (gsk_...): " KEY
  printf '{\n  "groq_api_key": "%s"\n}\n' "$KEY" > config.json
  chmod 600 config.json
  echo "✓ Key saved to config.json"
else
  echo "✓ config.json already exists"
fi

echo ""
echo "== Setup done. Start it with:  bash run.sh =="
echo ""
echo "macOS will ask for permissions on first run — grant ALL of these to Terminal"
echo "(System Settings → Privacy & Security):"
echo "  • Microphone         (to hear you)"
echo "  • Input Monitoring   (to detect the Right Option hotkey)"
echo "  • Accessibility      (to paste text at your cursor)"
echo "After granting, quit and reopen Terminal, then run:  bash run.sh"
