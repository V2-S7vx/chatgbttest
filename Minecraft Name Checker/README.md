# Minecraft Name Checker

A GUI application to check Minecraft username availability using namemc.com

## Features

- 🔍 **Multiple Check Modes:**
  - All combinations (3-5 characters)
  - 3-letter combinations (letters + numbers)
  - 4-letter combinations (letters + numbers)
  - 3/4/5 letter real English words
  - Custom word lists

- 🎯 **Smart Availability Checking**
  - Uses namemc.com API for accurate results
  - Rate limiting with configurable delay
  - Concurrent checks for speed
  - Automatic retry on rate limits

- 🔔 **Notifications**
  - Sound notification when available name found
  - Auto-copy to clipboard option
  - System tray support

- 📊 **Results Management**
  - Real-time results table with timestamps
  - Export to TXT, CSV, or JSON
  - Copy individual names with one click
  - Activity log with timestamps

- 🎨 **Modern Dark UI**
  - Discord-inspired dark theme
  - System tray support
  - Pause/resume/stop controls
  - Progress tracking

## Requirements

- Python 3.8+
- PySide6
- aiohttp

## Installation

1. Install Python 3.8+ from [python.org](https://python.org)
2. Run `startup.bat` (it will install dependencies automatically)
   Or manually:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Copy `.env.example` to `.env` and configure:

```env
# Optional: Discord webhook for notifications
DISCORD_WEBHOOK_URL=your_webhook_url

# Check delay (seconds)
CHECK_DELAY=0.5

# Max concurrent requests
MAX_CONCURRENT=3

# Sound notifications
SOUND_ENABLED=true

# Auto-copy available names to clipboard
AUTO_COPY=false
```

## Usage

1. Run `startup.bat` or `python mc_name_checker.py`
2. Select check mode from dropdown
3. Adjust delay if needed (0.5s recommended)
3. Click **Start Checking**
4. Monitor results in the table and activity log
4. Click **Copy** to copy available names
5. Use **Export Results** to save found names

## Check Modes

| Mode | Description | Count |
|------|-------------|-------|
| All Combinations | All 3-5 char combos (letters + numbers) | ~1.7M |
| 3-Letter Combos | All 3-char combos (a-z, 0-9) | 46,656 |
| 4-Letter Combos | All 4-char combos (a-z, 0-9) | 1.6M |
| 3-Letter Words | Real English 3-letter words | 257 |
| 4-Letter Words | Real English 4-letter words | 190 |
| 5-Letter Words | Real English 5-letter words | 170 |
| Custom List | Your own word list | Custom |

## API Sources

- **Primary:** namemc.com (via public API)
- Checks profile existence to determine availability
- Respects rate limits automatically

## Screenshots

The app features a modern dark theme with:
- Real-time results table with copy buttons
- Live activity log with color-coded messages
- Progress bar with rate estimation
- System tray support for background operation

## Troubleshooting

**"No names found"**
- Check your internet connection
- Reduce check delay if getting rate limited
- Try different check modes

**"Module not found" errors**
- Run `pip install -r requirements.txt`
- Ensure Python 3.8+ is installed

**Rate limited by namemc**
- Increase CHECK_DELAY in .env
- Reduce MAX_CONCURRENT
- Wait and try again

## License

MIT License - Feel free to modify and distribute