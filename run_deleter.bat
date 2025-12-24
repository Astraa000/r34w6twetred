@echo off
echo Installing requirements...
pip install -r requirements.txt >nul 2>&1
cls
python discord_deleter/deleter.py
pause
