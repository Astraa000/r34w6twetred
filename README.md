<div align="center">

# 🗑️ Discord Message Deleter

### *Lightning-fast bulk message deletion with intelligent auto-recovery*

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Discord](https://img.shields.io/badge/Discord-API-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[Features](#-features) • [Quick Start](#-quick-start) • [Configuration](#%EF%B8%8F-configuration) • [Documentation](#-documentation)

</div>

---

## 🌟 Features

<table>
<tr>
<td width="50%">

### ⚡️ **High Performance**
- Bulk message deletion with rate limit handling
- Concurrent processing for maximum speed
- Smart retry mechanism for failed deletions

</td>
<td width="50%">

### 🔄 **Auto-Recovery**
- Watchdog process monitors script health
- Automatic restart on crashes
- Zero data loss with checkpoint system

</td>
</tr>
<tr>
<td width="50%">

### 💾 **Smart Checkpointing**
- Resume from exact point of interruption
- Checkpoint every 10 deletions
- Progress persistence across sessions

</td>
<td width="50%">

### 🎯 **Flexible Targeting**
- Delete by date range
- Filter by specific channels
- Specify exact message count

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.7+
Discord User Token
```

### Installation

```bash
# Clone the repository
git clone https://github.com/Astraa000/r34w6twetred.git
cd r34w6twetred

# Install dependencies
pip install -r requirements.txt

# Configure your settings
cp config.json.example config.json
nano config.json
```

### 🎬 Run

**With Auto-Recovery (Recommended)**
```bash
python3 watchdog.py --auto
```

**Manual Mode**
```bash
python3 discord_deleter/deleter.py
```

---

## ⚙️ Configuration

Create a `config.json` file in the root directory:

```json
{
  "token": "YOUR_DISCORD_TOKEN",
  "channel_id": null,
  "delete_from_everywhere": true,
  "before_date": "2024-01-01T00:00:00Z",
  "after_date": null,
  "message_limit": null
}
```

### Configuration Options

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `token` | `string` | Your Discord user token | **Required** |
| `channel_id` | `string` | Specific channel ID to delete from | `null` (all channels) |
| `delete_from_everywhere` | `boolean` | Delete from all accessible channels | `true` |
| `before_date` | `string` | Delete messages before this date (ISO 8601) | `null` |
| `after_date` | `string` | Delete messages after this date (ISO 8601) | `null` |
| `message_limit` | `integer` | Maximum number of messages to delete | `null` (unlimited) |

---

## 📖 Documentation

### 🔍 Getting Your Discord Token

<details>
<summary><b>Click to expand token instructions</b></summary>

1. Open Discord in your web browser
2. Press `F12` to open Developer Tools
3. Go to the **Console** tab
4. Paste this code and press Enter:

```javascript
(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
```

5. Copy the token (exclude quotes)
6. Paste into your `config.json`

> **⚠️ Warning:** Never share your token with anyone. It provides full access to your Discord account.

</details>

---

### 🔄 How Auto-Recovery Works

The watchdog process monitors the deleter script and automatically restarts it if:
- Script crashes unexpectedly
- Network connection is lost
- Rate limits cause extended delays
- Process becomes unresponsive

**Architecture:**
```
┌─────────────────┐
│   Watchdog      │
│   Process       │
└────────┬────────┘
         │ monitors
         ▼
┌─────────────────┐      ┌──────────────┐
│   Deleter       │─────▶│  Checkpoint   │
│   Script        │      │  File         │
└─────────────────┘      └──────────────┘
```

---

### 📊 Progress Tracking

The script maintains a checkpoint file (`checkpoint.json`) that stores:
- Last successfully deleted message ID
- Last processed channel ID
- Total messages deleted
- Timestamp of last checkpoint

**Example checkpoint:**
```json
{
  "last_message_id": "1234567890123456789",
  "last_channel_id": "9876543210987654321",
  "messages_deleted": 1337,
  "timestamp": "2024-01-15T10:30:45Z"
}
```

---

### 🛠️ Advanced Usage

#### Using the Count Script

Count messages before deletion:

```bash
python3 count_messages.py
```

This will show you exactly how many messages will be deleted based on your `config.json` settings.

#### Running in Background

**macOS/Linux:**
```bash
nohup python3 watchdog.py --auto > deleter.log 2>&1 &
```

**Windows:**
```cmd
run_deleter.bat
```

**macOS (with Terminal Profile):**
```bash
chmod +x run_deleter.command
./run_deleter.command
```

---

## 📁 Project Structure

```
discord-message-deleter/
├─ 📄 README.md                  # This file
├─ 📋 requirements.txt           # Python dependencies
├─ ⚙️ config.json               # Your configuration (create this)
├─ 🔧 watchdog.py               # Auto-recovery watchdog
├─ 📊 count_messages.py         # Message counter utility
├─ 🪟 run_deleter.bat           # Windows launcher
├─ 🍎 run_deleter.command       # macOS launcher
└─ discord_deleter/
   ├─ 🚀 deleter.py             # Main deletion script
   └─ 📖 README.md              # Module documentation
```

---

## 🎯 Use Cases

- **Privacy Cleanup**: Delete old messages from all servers
- **Account Reset**: Clear message history before account transfer
- **Data Minimization**: Remove unnecessary message footprint
- **Testing**: Clean up test messages in development servers

---

## ⚠️ Important Notes

> **Rate Limits**: Discord enforces strict rate limits. The script automatically handles these, but deletion may take time for large message counts.

> **Deletable Messages**: You can only delete messages you sent. DMs and server messages you authored are fair game.

> **Permanent Action**: Deleted messages **cannot be recovered**. Use the count script first to verify scope.

---

## 🐛 Troubleshooting

<details>
<summary><b>Script stops with rate limit errors</b></summary>

This is normal. The watchdog will automatically restart the script after the cooldown period. You can also manually wait and restart.

</details>

<details>
<summary><b>Token authentication failed</b></summary>

Your token may have expired. Generate a new one using the instructions above and update `config.json`.

</details>

<details>
<summary><b>Checkpoint not resuming correctly</b></summary>

Delete `checkpoint.json` to start fresh. This will reset progress tracking.

</details>

<details>
<summary><b>Watchdog not detecting crashes</b></summary>

Ensure you're using `--auto` flag:
```bash
python3 watchdog.py --auto
```

</details>

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest features
- 🔨 Submit pull requests
- 📖 Improve documentation

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚡ Performance Stats

| Metric | Value |
|--------|-------|
| **Deletion Speed** | ~500-1000 messages/hour |
| **Recovery Time** | < 5 seconds |
| **Memory Usage** | ~50-100 MB |
| **Checkpoint Frequency** | Every 10 deletions |

---

## 🔗 Related Projects

- [Discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) - Export Discord chats

---

<div align="center">

### ⭐ Star this repo if it helped you!

**Made with 💜 by [Astraa](https://github.com/Astraa000)**

</div>
