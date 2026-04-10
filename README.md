# VirtualDJ Discord Rich Presence

A small Python script that shows your currently playing track from VirtualDJ as a Discord Rich Presence status, with album artwork fetched from iTunes.

## What it does

- Detects when VirtualDJ is running and connects to Discord automatically
- Reads the current track from VirtualDJ's history log
- Fetches album art from the iTunes API
- Shows elapsed mixing time
- Clears the status when VirtualDJ is closed

## Requirements

- **Python 3.8+** — [python.org/downloads](https://www.python.org/downloads/) (check "Add Python to PATH" during install)
- **Discord desktop app** — the browser version doesn't support Rich Presence
- **VirtualDJ** — any version that writes to a history file

## Setup

### 1. Create a Discord Application

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application**
3. Name it whatever you want — this name shows up as "Playing **YourName**" on your profile (e.g. `VirtualDJ`)
4. Click **Create**

### 2. Get your Client ID

1. On your application page, go to **General Information**
2. Copy the **Application ID** (long number)

### 3. Add a fallback image (optional)

If no album art is found on iTunes, the script falls back to an image asset called `virtualdj_logo`. To set it up:

1. In the Developer Portal, go to **Rich Presence → Art Assets**
2. Upload a square image (512×512px or larger)
3. Name it exactly `virtualdj_logo`
4. Save

### 4. Configure the script

Open `main.py` and replace the Client ID on line 14:

```python
CLIENT_ID = "YOUR_CLIENT_ID_HERE"
```

Paste your Application ID between the quotes.

### 5. Configure VirtualDJ (recommended)

By default, VirtualDJ waits 45 seconds before writing a track to the history file. You probably want to lower this so your Discord status updates faster.

1. Open VirtualDJ → **Settings** → **Options**
2. Search for `historyDelay`
3. Set it to `0` (instant) or `5` (slight delay to skip previewed tracks)

## Usage

**Windows:** Double-click `start.bat`. It installs dependencies automatically on first run.

**Manual:**
```bash
pip install -r requirements.txt
python main.py
```

The script runs in a loop — it waits for VirtualDJ to open, connects to Discord, and updates the track in real time. Close the terminal or press `Ctrl+C` to stop.

## How it works

The script polls every 10 seconds:

1. Checks if `virtualdj.exe` is running (via `psutil`)
2. Reads the last line of `~/Documents/VirtualDJ/History/tracklist.txt`
3. Searches iTunes for matching album art
4. Pushes the info to Discord via `pypresence`

When VirtualDJ closes, it clears the Discord status and goes back to waiting.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Discord is not running" | Open the Discord **desktop** app (not browser) |
| "Invalid Client ID" | Make sure you copied the Application ID, not the Public Key |
| Track doesn't update | Set `historyDelay` to `0` in VirtualDJ settings |
| Script won't start | Check that Python is in your PATH: `python --version` |

## License

MIT
