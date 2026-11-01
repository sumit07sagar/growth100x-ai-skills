#!/bin/bash
# the assistant / Meeting Notetaker one-time setup. Run: bash setup.sh
set -e
cd "$(dirname "$0")"

echo "== Meeting Notetaker (the assistant) setup =="

if ! command -v python3 &>/dev/null; then
  echo "python3 not found. Install Xcode Command Line Tools first: xcode-select --install"
  exit 1
fi

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
./.venv/bin/pip install --quiet --upgrade pip
./.venv/bin/pip install --quiet sounddevice numpy requests
echo "✓ Dependencies installed"

if [ -f "../VoiceType/config.json" ]; then
  echo "✓ Reusing your Groq API key from ../VoiceType/config.json — no need to create a new one."
elif [ ! -f "config.json" ]; then
  echo ""
  echo "Get a FREE API key at: https://console.groq.com/keys (sign up with Google, no card needed)"
  read -p "Paste your Groq API key (gsk_...): " KEY
  printf '{\n  "groq_api_key": "%s"\n}\n' "$KEY" > config.json
  chmod 600 config.json
  echo "✓ Key saved to config.json"
else
  echo "✓ config.json already exists"
fi

mkdir -p Transcripts

echo ""
echo "== Setup done =="
echo ""
echo "IMPORTANT: you still need the ONE-TIME audio routing setup before your"
echo "first meeting — see README.md for exact steps (BlackHole + Multi-Output"
echo "+ Aggregate Device). This only needs to be done once, ever, per audio"
echo "setup you use (built-in / wired / Bluetooth)."
echo ""
echo "macOS will ask for Microphone permission for Terminal on first run — grant it."
