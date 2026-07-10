# Lidarr Releases to ntfy

Small Python script that checks today's album releases from Lidarr and sends a single grouped notification to an ntfy topic. It queries Lidarr's calendar endpoint for the current day and publishes the result with a standard HTTP POST request.

## Features

- Fetches albums releasing today from Lidarr's calendar API.
- Sends one grouped notification to an ntfy topic.
- Uses environment variables for configuration.
- Supports public ntfy topics and self-hosted ntfy servers.
- Supports optional ntfy authentication for protected topics.
- Simple setup with a single `app.py` file.

## Files

- `app.py` — main script.
- `.env.sample` — example environment configuration.
- `requirements.txt` — pinned Python dependencies.

## Requirements

- Python 3.9+ recommended.
- A running Lidarr instance with an API key from **Settings > General**.
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

# Optional, only if your ntfy topic requires authentication
NTFY_USERNAME=""
NTFY_PASSWORD=""
NTFY_TOKEN=""
```

### Variables

- `LIDARR_URL` — base URL of your Lidarr instance.
- `LIDARR_API_KEY` — Lidarr API key.
- `NTFY_URL` — full ntfy topic URL to publish notifications to.
- `NTFY_USERNAME` — optional ntfy username for Basic auth.
- `NTFY_PASSWORD` — optional ntfy password for Basic auth.
- `NTFY_TOKEN` — optional ntfy access token for Bearer auth.

Use either `NTFY_TOKEN` or the `NTFY_USERNAME` / `NTFY_PASSWORD` pair when your ntfy server requires authentication.

## Installation

1. Clone or copy the project files.
2. Create a virtual environment.
3. Install the required dependencies from `requirements.txt`.
4. Copy `.env.sample` to `.env` and update the values.

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

The script will:

1. Read configuration from `.env`.
2. Call Lidarr's `/api/v1/calendar` endpoint for today's releases.
3. Build a grouped notification message from the returned albums.
4. Send the message to ntfy with an HTTP POST request.
5. Exit without sending anything if no albums are returned.

## Example notification

```text
Albums released today:
- Artist 1 — Album 1 (2026-07-07)
- Artist 2 — Album 2 (2026-07-07)
```

## How it works

Lidarr exposes a calendar endpoint that can be filtered with `start` and `end` query parameters, and the API docs expose calendar and artist-related endpoints for this kind of lookup. ntfy accepts direct HTTP publishing and supports headers such as `Title`, `Tags`, and `Priority`, which makes it easy to integrate into small automation scripts. [web:23][web:1]

## Automation

You can run the script from:

- `cron` on Linux.
- Home Assistant via `shell_command` or a scheduled automation.
- A scheduled Docker job.
- A CI runner or any other scheduler that can execute Python.

### Example cron entry

```cron
5 9 * * * /path/to/.venv/bin/python /path/to/app.py
```

## Self-hosted ntfy notes

If you use a self-hosted ntfy server, replace `https://ntfy.sh/YOUR_TOPIC` with your own topic URL. If the topic is protected, configure authentication in `.env`, because ntfy supports authenticated publishing and protected topics can reject anonymous writes with HTTP 403. [web:1]

## Troubleshooting

### `403 Client Error: Forbidden` when posting to ntfy

This usually means the script reached ntfy successfully, but ntfy refused the publish request. ntfy documents simple POST publishing, and protected or read-only topics can return 403 when credentials are missing or topic permissions deny writes. [web:1]

Common causes:

- The topic is not writable anonymously.
- Your self-hosted ntfy server requires authentication.
- Topic ACLs or default access rules deny publishing.
- The URL points to the correct topic, but the credentials are missing or invalid.

Quick checks:

```bash
curl -d "test" "$NTFY_URL"
curl -u username:password -d "test" "$NTFY_URL"
```

If the authenticated request works and the anonymous one fails, add `NTFY_USERNAME` / `NTFY_PASSWORD` or `NTFY_TOKEN` to your `.env` and update `app.py` to send the matching auth headers.

### No notification sent

If there are no albums in Lidarr's calendar response for today, the script should exit cleanly without publishing a message.

### Lidarr request fails

Check that:

- `LIDARR_URL` is correct.
- `LIDARR_API_KEY` is valid.
- Lidarr is reachable from the machine running the script.

## Suggested `.env.sample`

```env
LIDARR_URL="http://IP:8686"
LIDARR_API_KEY="APIKEY"

NTFY_URL="https://ntfy.sh/YOUR_TOPIC"
NTFY_USERNAME=""
NTFY_PASSWORD=""
NTFY_TOKEN=""
```

## Notes

- Public ntfy topics can work with only `NTFY_URL`.
- Protected ntfy topics need authentication.
- `python-dotenv` 1.2.2 is a current release as of March 2026. [web:22]
- If you prefer one notification per album, you can loop over the results and publish once per album instead of sending one grouped message.