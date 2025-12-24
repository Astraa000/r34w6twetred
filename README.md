# Discord Message Deleter

A robust Discord message deletion tool with automatic recovery and checkpoint resume capabilities.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Auto-Recovery System** - Watchdog process monitors deletion and auto-restarts on failures
- **Checkpoint Resume** - Automatically saves progress and resumes from last position
- **Smart Rate Limiting** - Exponential backoff with Discord retry-after header support
- **Verification Scanning** - Multiple verification passes ensure complete deletion
- **Persistent Statistics** - Track total deletions across all sessions
- **Comprehensive Logging** - Detailed logs with automatic rotation

## Installation

**Requirements:**
- Python 3.7 or higher
- Discord user account token

**Setup:**

```bash
git clone https://github.com/yourusername/discord-message-deleter.git
cd discord-message-deleter
pip3 install -r requirements.txt
```

## Configuration

### Getting Your Discord Token

1. Open Discord in your browser (https://discord.com/app)
2. Open Developer Tools (F12)
3. Navigate to Console tab
4. Execute:

```javascript
(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
```

5. Copy the returned token

### Getting Channel ID

1. Enable Developer Mode: Settings → Advanced → Developer Mode
2. Right-click on any message in target channel
3. Select "Copy Message Link"
4. Extract channel ID from URL: `discord.com/channels/@me/{CHANNEL_ID}/...`

### Getting User ID

1. Enable Developer Mode (if not already enabled)
2. Right-click your username
3. Select "Copy User ID"

## Usage

### Interactive Mode

```bash
python3 discord_deleter/deleter.py
```

First run will prompt for:
- Discord token
- Channel ID
- User ID

Configuration is saved to `config.json` for subsequent runs.

### Automated Mode (Recommended)

```bash
python3 watchdog.py --auto
```

Runs with watchdog monitoring for automatic recovery on crashes.

### Message Counting

```bash
python3 count_messages.py
```

Scans and displays total message count without deletion.

## Architecture

```
┌─────────────────────────────────────┐
│         Watchdog Process            │
│                                     │
│  ┌───────────────────────────────┐ │
│  │    Deletion Process            │ │
│  │                                │ │
│  │  • Fetch messages (batch 100)  │ │
│  │  • Filter user messages        │ │
│  │  • Delete with rate limiting   │ │
│  │  • Save checkpoint             │ │
│  └───────────────────────────────┘ │
│           │                         │
│           │ (on failure)            │
│           ↓                         │
│  Auto-restart from checkpoint       │
└─────────────────────────────────────┘
```

### Deletion Modes

**Mode 1: Scan-First (Safe)**
- Scans all messages before deletion
- Displays statistics
- Requires confirmation

**Mode 2: Stream Deletion (Fast)**
- Deletes messages as discovered
- Default mode for `--auto` flag
- Recommended for large deletions

## Performance

**Deletion Rate:** 8-30 messages per minute

Rate limited to balance speed with account safety. Discord's API has strict rate limits and automated detection systems.

**Configuration:** Delays can be adjusted in `deleter.py` (lines 47-54), though this increases detection risk.

## Rate Limiting

The tool implements multiple rate limiting strategies:

1. **Fixed Delays** - Base delay between deletion operations
2. **Exponential Backoff** - Increasing delays on repeated rate limits
3. **Retry-After Headers** - Respects Discord's rate limit headers
4. **Random Jitter** - Randomized delays to avoid pattern detection

## Risk Assessment

**IMPORTANT:** This tool performs automated actions on a user account, which violates Discord's Terms of Service.

**Potential Consequences:**
- Account suspension (temporary or permanent)
- Loss of Discord Nitro subscription
- Loss of all server memberships and data

**Risk Factors:**
- Number of messages deleted
- Deletion speed
- Account age and activity
- Previous violations

Use at your own risk. No warranty or liability is provided.

## Configuration File

After initialization, settings are stored in `config.json`:

```json
{
    "token": "YOUR_DISCORD_TOKEN",
    "channel_id": "CHANNEL_ID",
    "user_id": "YOUR_USER_ID",
    "total_deleted": 0,
    "last_message_id": null
}
```

**Security:** Never commit `config.json` to version control. The token provides full account access.

## Logging

**Deletion Logs:** `deleter.log`
- Rotated automatically after 1000 lines
- Contains deletion progress and errors

**Watchdog Logs:** Console output
- Monitors process status
- Tracks restart events

## Troubleshooting

### Authentication Errors (401/403)

Token is invalid or expired. Obtain a new token and update `config.json`.

### Persistent Rate Limiting

Discord has flagged your activity. Consider:
- Reducing deletion speed
- Taking longer breaks between sessions
- Using a different account

### Watchdog Restart Loop

Check logs for error patterns:
- **Auth errors:** Token is invalid
- **Network errors:** Connection issues
- **Rate limit errors:** Excessive requests

### Mode 1 NameError

Chat analysis feature is currently disabled. Use Mode 2 instead.

## Project Structure

```
.
├── discord_deleter/
│   └── deleter.py          # Core deletion engine
├── watchdog.py             # Auto-recovery monitor
├── count_messages.py       # Message counting utility
├── config.json             # User configuration (generated)
├── deleter.log             # Deletion logs
├── requirements.txt        # Python dependencies
├── run_deleter.command     # macOS launcher
└── run_deleter.bat         # Windows launcher
```

## Comparison

| Feature | This Tool | Standard Tools |
|---------|-----------|----------------|
| Auto-restart on crash | Yes | No |
| Checkpoint resume | Yes | No |
| Extended sessions (24h+) | Yes | Limited |
| Rate limit handling | Advanced | Basic |
| Progress persistence | Yes | No |

## Contributing

Contributions are welcome. Areas of interest:

- GUI implementation
- Message export/backup functionality
- Performance optimizations
- Multi-account support
- Enhanced error recovery

## License

MIT License - See LICENSE file for details.

## Disclaimer

This software is provided "as-is" without warranty of any kind. The developer assumes no liability for:

- Account suspensions or bans
- Data loss
- Violation of Discord Terms of Service
- Any other consequences of use

Users assume full responsibility for all risks associated with using this tool.

**Discord Terms of Service explicitly prohibit automated user account actions ("self-botting"). Use of this tool may result in account termination.**

## Technical Notes

**API Endpoints Used:**
- `GET /api/v9/channels/{channel_id}/messages` - Message retrieval
- `DELETE /api/v9/channels/{channel_id}/messages/{message_id}` - Message deletion

**Rate Limits:**
- Message fetching: ~50 requests per second
- Message deletion: ~5 requests per second (conservative)

**Dependencies:**
- `requests` - HTTP client
- `colorama` - Cross-platform colored terminal output

---

**Status:** Production-ready. Tested with 30,000+ message deletions over extended sessions.
