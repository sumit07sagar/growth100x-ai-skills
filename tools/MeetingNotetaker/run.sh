#!/bin/bash
# Start a meeting recording. Keep this Terminal window open during the call.
cd "$(dirname "$0")"
[ -d ".venv" ] || { echo "Run bash setup.sh first."; exit 1; }
read -p "Client / meeting name (optional, press Enter to skip): " NAME
exec ./.venv/bin/python3 meeting_recorder.py "${NAME:-Meeting}"
