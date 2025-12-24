#!/usr/bin/env python3
"""
Discord Deleter Watchdog
Monitors and automatically restarts the deleter if it crashes
"""
import subprocess
import time
import sys
import os
from datetime import datetime
from pathlib import Path

# Configuration
DELETER_SCRIPT = "discord_deleter/deleter.py"
LOG_FILE = "deleter.log"
MAX_LOG_LINES = 1000
CHECK_INTERVAL = 5  # seconds
RESTART_DELAY = 3  # seconds before restarting after crash

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m' + '\033[1m'
    CYAN = '\033[96m' + '\033[1m'
    GREEN = '\033[92m' + '\033[1m'
    YELLOW = '\033[93m' + '\033[1m'
    RED = '\033[91m' + '\033[1m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def log(message, color=Colors.RESET):
    """Log message to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(f"{color}{formatted}{Colors.RESET}")
    
    # Append to log file
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
        
        # Rotate log if too large
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if len(lines) > MAX_LOG_LINES:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.writelines(lines[-MAX_LOG_LINES:])
    except Exception as e:
        print(f"{Colors.RED}Failed to write log: {e}{Colors.RESET}")

def check_script_exists():
    """Verify deleter script exists"""
    if not os.path.exists(DELETER_SCRIPT):
        log(f"ERROR: Deleter script not found: {DELETER_SCRIPT}", Colors.RED)
        log(f"Please ensure you're running watchdog from the correct directory", Colors.RED)
        sys.exit(1)

def run_deleter():
    """Run the deleter script"""
    log("Starting Discord Deleter...", Colors.GREEN)
    
    try:
        # Run deleter
        process = subprocess.Popen(
            [sys.executable, DELETER_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        return process
    except Exception as e:
        log(f"Failed to start deleter: {e}", Colors.RED)
        return None

def monitor_process(process):
    """Monitor process output and status"""
    last_output = time.time()
    
    try:
        while True:
            # Check if process is still running
            if process.poll() is not None:
                return process.returncode
            
            # Read output
            line = process.stdout.readline()
            if line:
                log(line.rstrip(), Colors.CYAN)
                last_output = time.time()
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        log("Watchdog interrupted by user", Colors.YELLOW)
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
        raise

def main():
    """Main watchdog loop"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("="*60)
    print("   DISCORD DELETER WATCHDOG")
    print("   Auto-Recovery System Active")
    print("="*60)
    print(Colors.RESET)
    
    log("Watchdog initialized", Colors.GREEN)
    log(f"Monitoring: {DELETER_SCRIPT}", Colors.CYAN)
    log(f"Logs: {LOG_FILE}", Colors.CYAN)
    log(f"Press Ctrl+C to stop watchdog", Colors.YELLOW)
    print()
    
    check_script_exists()
    
    restart_count = 0
    consecutive_auth_failures = 0
    max_consecutive_auth_failures = 3
    max_total_restarts = 10
    
    try:
        while True:
            process = run_deleter()
            
            if process is None:
                log("Failed to start deleter. Retrying in 10 seconds...", Colors.RED)
                time.sleep(10)
                continue
            
            # Monitor the process
            exit_code = monitor_process(process)
            
            # Check exit code
            if exit_code == 0:
                log("Deleter exited normally (complete)", Colors.GREEN)
                log("All deletions complete. Watchdog shutting down.", Colors.GREEN)
                break
            elif exit_code == 2:
                log("Deleter exited (user cancelled, no deletes)", Colors.YELLOW)
                log("Watchdog shutting down.", Colors.YELLOW)
                break
            elif exit_code == 1:
                # Auth error - likely token invalid
                consecutive_auth_failures += 1
                restart_count += 1
                log(f"Deleter crashed with auth error (exit code 1)", Colors.RED)
                log(f"Consecutive auth failures: {consecutive_auth_failures}/{max_consecutive_auth_failures}", Colors.YELLOW)
                
                if consecutive_auth_failures >= max_consecutive_auth_failures:
                    log("CRITICAL: Too many consecutive auth failures!", Colors.RED)
                    log("Your token is likely invalid or expired.", Colors.RED)
                    log("Please check config.json and verify your Discord token.", Colors.RED)
                    log("Watchdog shutting down to prevent account hammering.", Colors.RED)
                    sys.exit(1)
                
                log(f"Auto-restart #{restart_count} in {RESTART_DELAY} seconds...", Colors.YELLOW)
                time.sleep(RESTART_DELAY)
            else:
                # Other error - reset auth failure counter (temporary network issue, etc.)
                consecutive_auth_failures = 0
                restart_count += 1
                log(f"Deleter crashed with exit code {exit_code}", Colors.RED)
                
                # Check if we've exceeded total restart limit
                if restart_count >= max_total_restarts:
                    log("CRITICAL: Too many total restarts!", Colors.RED)
                    log(f"Restarted {restart_count} times without success.", Colors.RED)
                    log("There may be a persistent issue. Please check logs and config.", Colors.RED)
                    log("Watchdog shutting down.", Colors.RED)
                    sys.exit(1)
                
                log(f"Auto-restart #{restart_count} in {RESTART_DELAY} seconds...", Colors.YELLOW)
                time.sleep(RESTART_DELAY)
    
    except KeyboardInterrupt:
        log("\nWatchdog stopped by user", Colors.YELLOW)
        sys.exit(0)
    except Exception as e:
        log(f"Watchdog error: {e}", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()
