import time
import sys
import os
import psutil
import urllib.request
import urllib.parse
import json
from pypresence import Presence

# ==============================================================================
# Replace with your own Discord Application ID (Client ID).
# You can find it at https://discord.com/developers/applications
# ==============================================================================
CLIENT_ID = "YOUR_CLIENT_ID_HERE"

def is_virtualdj_running():
    """Check if a VirtualDJ process is currently running."""
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and 'virtualdj' in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def get_current_song():
    """Read the most recent track from VirtualDJ's history file."""
    history_file = os.path.expanduser(r"~\Documents\VirtualDJ\History\tracklist.txt")
    if not os.path.exists(history_file):
        return None

    try:
        with open(history_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in reversed(lines):
                line = line.strip()
                if not line or line.startswith("VirtualDJ History") or line.startswith("---"):
                    continue
                if " : " in line:
                    parts = line.split(" : ", 1)
                    if len(parts) == 2:
                        return parts[1]
        return None
    except Exception:
        return None

def get_album_art_url(song_title):
    """Fetch album artwork URL from the iTunes Search API."""
    try:
        query = urllib.parse.quote(song_title)
        url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data['resultCount'] > 0:
                artwork_url = data['results'][0]['artworkUrl100']
                return artwork_url.replace('100x100bb', '512x512bb')
    except Exception:
        pass

    return "virtualdj_logo"

def main():
    if CLIENT_ID == "YOUR_CLIENT_ID_HERE":
        print("Error: You need to set your Client ID in main.py first.")
        input("Press Enter to exit...")
        sys.exit(1)

    print("Starting VirtualDJ Rich Presence...")
    RPC = None
    connected = False
    start_time = None
    last_song = None

    print("Waiting for VirtualDJ to open. Press Ctrl+C to quit.\n")

    while True:
        try:
            vdj_running = is_virtualdj_running()
            current_song = get_current_song() if vdj_running else None

            # VirtualDJ just opened
            if vdj_running and not connected:
                print("VirtualDJ detected, connecting to Discord...")
                RPC = Presence(CLIENT_ID)
                RPC.connect()
                start_time = int(time.time())

                details_text = current_song if current_song else "On VirtualDJ"
                img_url = get_album_art_url(current_song) if current_song else "virtualdj_logo"

                RPC.update(
                    state="Mixing",
                    details=details_text,
                    large_image=img_url,
                    large_text="VirtualDJ",
                    start=start_time
                )
                connected = True
                last_song = current_song
                print("Connected to Discord.")
                if current_song:
                    print(f"Now playing: {current_song}")

            # VirtualDJ is running and the track changed
            elif vdj_running and connected:
                if current_song != last_song:
                    details_text = current_song if current_song else "On VirtualDJ"
                    img_url = get_album_art_url(current_song) if current_song else "virtualdj_logo"
                    try:
                        RPC.update(
                            state="Mixing",
                            details=details_text,
                            large_image=img_url,
                            large_text="VirtualDJ",
                            start=start_time
                        )
                        last_song = current_song
                        print(f"Now playing: {current_song}")
                    except Exception:
                        pass

            # VirtualDJ was closed
            elif not vdj_running and connected:
                print("VirtualDJ closed, clearing status...")
                try:
                    RPC.clear()
                    RPC.close()
                except Exception:
                    pass
                RPC = None
                connected = False
                start_time = None
                last_song = None
                print("Status cleared. Waiting for VirtualDJ...\n")

            time.sleep(10)

        except Exception as e:
            if "Pipe Not Found" in str(e) or "Not Found" in str(e):
                print("Discord is not running. Retrying...")
            elif "Client ID is Invalid" in str(e):
                print("Error: Invalid Client ID. Check your Application ID.")
            else:
                pass

            if RPC:
                try:
                    RPC.close()
                except Exception:
                    pass
                RPC = None
            connected = False
            last_song = None
            time.sleep(15)

if __name__ == "__main__":
    main()
