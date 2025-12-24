#!/usr/bin/env python3
"""Quick message counter - runs while deleter is active"""
import requests
import json
import sys
import time

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

token = config["token"]
channel_id = config["channel_id"]
user_id = config["user_id"]

# Setup session
session = requests.Session()
session.headers.update({"Authorization": token})

print("\n🔍 Counting remaining messages...")
print(f"Channel: {channel_id}")
print(f"User: {user_id}")
print("-" * 50)

base_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
count = 0
last_id = None
batch_num = 0

try:
    while True:
        params = {"limit": 100}
        if last_id:
            params["before"] = last_id
        
        r = session.get(base_url, params=params, timeout=30)
        
        if r.status_code != 200:
            if r.status_code == 429:
                retry_after = r.json().get('retry_after', 2)
                print(f"Rate limited, waiting {retry_after:.1f}s...")
                time.sleep(retry_after)
                continue
            else:
                print(f"Error {r.status_code}: {r.text}")
                break
        
        messages = r.json()
        if not messages:
            break
        
        # Count user's messages
        user_messages = [m for m in messages if m['author']['id'] == str(user_id)]
        count += len(user_messages)
        last_id = messages[-1]['id']
        batch_num += 1
        
        # Progress update
        print(f"\rBatch {batch_num}: {count} messages found (oldest: {last_id})", end="", flush=True)
        
        time.sleep(0.05)  # Small delay to avoid rate limits
    
    print(f"\n\n{'='*50}")
    print(f"✅ TOTAL REMAINING: {count:,} messages")
    
    # Calculate ETA based on current rate (~27 msgs/min)
    estimated_rate = 27  # msgs per minute
    estimated_minutes = count / estimated_rate
    hours = int(estimated_minutes // 60)
    minutes = int(estimated_minutes % 60)
    
    if hours > 0:
        eta = f"{hours}h {minutes}m"
    else:
        eta = f"{minutes}m"
    
    print(f"⏱️  ETA at ~{estimated_rate} msgs/min: {eta}")
    print(f"{'='*50}\n")

except KeyboardInterrupt:
    print(f"\n\n⚠️  Count interrupted at {count:,} messages")
except Exception as e:
    print(f"\n\n❌ Error: {e}")
