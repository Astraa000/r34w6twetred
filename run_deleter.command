#!/bin/bash
cd "$(dirname "$0")"

echo "Installing requirements..."
pip3 install -r requirements.txt >/dev/null 2>&1
clear

echo "🌙 Anti-Sleep Mode Active: System will stay awake while this runs."
caffeinate -i python3 discord_deleter/deleter.py

echo ""
echo "Program exited."
read -p "Press ENTER to close this window..."
