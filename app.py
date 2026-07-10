import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

LIDARR_URL = os.getenv("LIDARR_URL")
LIDARR_API_KEY = os.getenv("LIDARR_API_KEY")
NTFY_URL = os.getenv("NTFY_URL")

NTFY_USERNAME = os.getenv("NTFY_USERNAME")
NTFY_PASSWORD = os.getenv("NTFY_PASSWORD")
NTFY_TOKEN = os.getenv("NTFY_TOKEN")

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
    artist = album.get("artist", {}).get("artistName", "")
    title = album.get("title", "Unknown album")
    release = album.get("releaseDate", "")[:10]
    lines.append(f"- {artist} — {title} ({release})" if artist else f"- {title} ({release})")

message = "Albums released today:\n" + "\n".join(lines)

headers = {
    "Title": f"Lidarr releases for {today.isoformat()}",
    "Tags": "music,cd",
    "Priority": "default",
}

if NTFY_TOKEN:
    headers["Authorization"] = f"Bearer {NTFY_TOKEN}"

auth = None
if NTFY_USERNAME and NTFY_PASSWORD and not NTFY_TOKEN:
    auth = (NTFY_USERNAME, NTFY_PASSWORD)

ntfy_resp = requests.post(
    NTFY_URL,
    headers=headers,
    data=message.encode("utf-8"),
    auth=auth,
    timeout=30,
)
ntfy_resp.raise_for_status()