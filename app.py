import os

import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv, dotenv_values
load_dotenv()

LIDARR_URL = os.getenv("LIDARR_URL")
LIDARR_API_KEY = os.getenv("LIDARR_API_KEY")

NTFY_URL = os.getenv("NTFY_URL")

today = datetime.now().date()
tomorrow = today + timedelta(days=1)

resp = requests.get(
    f"{LIDARR_URL}/api/v1/calendar",
    headers={"X-Api-Key": LIDARR_API_KEY},
    params={
        "start": today.isoformat(),
        "end": tomorrow.isoformat(),
        "includeArtist": "true",
        "unmonitored": "false",
    },
    timeout=30,
)
resp.raise_for_status()
albums = resp.json()

if not albums:
    raise SystemExit(0)

lines = []
for album in albums:
    artist = ""
    if album.get("artist"):
        artist = album["artist"].get("artistName", "")
    title = album.get("title", "Unknown album")
    release = album.get("releaseDate", "")[:10]
    if artist:
        lines.append(f"- {artist} — {title} ({release})")
    else:
        lines.append(f"- {title} ({release})")

message = "Albums released today:\n" + "\n".join(lines)

ntfy_resp = requests.post(
    NTFY_URL,
    headers={
        "Title": f"Lidarr releases for {today.isoformat()}",
        "Tags": "music,cd",
        "Priority": "default",
    },
    data=message.encode("utf-8"),
    timeout=30,
)
ntfy_resp.raise_for_status()