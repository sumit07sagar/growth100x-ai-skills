#!/bin/bash
# Start VoiceType. Keep this Terminal window open while dictating.
cd "$(dirname "$0")"
[ -d ".venv" ] || { echo "Run  bash setup.sh  first."; exit 1; }
exec ./.venv/bin/python3 voicetype.py
