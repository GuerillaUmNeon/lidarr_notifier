# Lidarr Releases to ntfy

Small Python script that checks **today's album releases** from Lidarr and sends a notification to an ntfy topic. The script queries Lidarr's calendar endpoint and publishes a message through ntfy using a standard HTTP POST request.

## Features

- Fetches albums releasing **today** from Lidarr's calendar API.
- Sends one grouped notification to an ntfy topic.
- Uses environment variables for configuration.
- Simple setup with a single `app.py` file.

## Files

- `app.py` — main script.
- `.env.sample` — example environment configuration.
- `requirements.txt` — pinned Python dependencies.

## Requirements

- Python 3.9+ recommended.
- A running Lidarr instance with an API key generated from Settings > General.
- An ntfy topic URL, either on [ntfy.sh](https://ntfy.sh) or a self-hosted ntfy server.
- The Python packages listed in `requirements.txt`:
  - `python-dotenv==1.2.2`
  - `requests==2.34.2`

## Environment variables

Create a `.env` file based on `.env.sample`:

```env
LIDARR_URL="http://IP:8686"
LIDARR_API_KEY="APIKEY"

NTFY_URL="https://ntfy.sh/YOUR_TOPIC"
```

Variable details:

- `LIDARR_URL` — base URL of your Lidarr instance.
- `LIDARR_API_KEY` — Lidarr API key.
- `NTFY_URL` — full ntfy topic URL to publish notifications to.

## Installation

1. Clone or copy the project files.
2. Create a virtual environment.
3. Install the required dependencies from `requirements.txt`.
4. Copy `.env.sample` to `.env` and update the values.

Example:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
```

## Usage

Run the script manually with:

```bash
python3 app.py
```

The script should:

1. Read configuration from `.env`.
2. Call Lidarr's `/api/v1/calendar` endpoint for today's releases using the API key.
3. Build a notification message from the returned albums.
4. Send the message to ntfy with an HTTP POST request.

## Example notification

```text
Albums released today:
- Artist 1 — Album 1 (2026-07-07)
- Artist 2 — Album 2 (2026-07-07)
```

## How it works

Lidarr exposes a calendar API that accepts `start` and `end` query parameters, which makes it suitable for filtering albums released today. ntfy accepts plain HTTP POST publishing with optional headers like `Title`, `Tags`, and `Priority`, which makes it easy to integrate with scripts and automation tools.

## Automation ideas

This script can be triggered from:

- Home Assistant via `shell_command` or a scheduled automation.
- cron on Linux.
- Docker scheduled jobs.
- A CI runner or any scheduler that can execute Python.

## Notes

- If no albums are returned for today, the script can safely exit without sending a notification.
- If you use a self-hosted ntfy server, replace `https://ntfy.sh/YOUR_TOPIC` with your own server URL.
- If you want one notification per album instead of one grouped message, adjust the script to POST once per result.
