# Freshdesk Private Connector

This project implements a read-only Freshdesk connector for an Agent Studio agent. It supports only the required ticket operations: list tickets, get a ticket, and search tickets.

## Requirements

- Python 3.10+
- `pip install -r requirements.txt`

## Setup

1. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
2. Fill in your Freshdesk credentials:
   ```env
   FRESHDESK_DOMAIN=https://your-subdomain.freshdesk.com
   FRESHDESK_API_KEY=your_api_key_here
   ```
3. Install package dependencies:
   ```bash
   python -m pip install -r requirements.txt
   python -m pip install -e .
   ```

## Authentication

This connector uses Freshdesk API-key authentication (Basic Auth). Freshdesk API keys are read from the environment variables `FRESHDESK_DOMAIN` and `FRESHDESK_API_KEY`.

This connector does not implement OAuth because Freshdesk direct API access for this scope is API-key based, and the assignment explicitly requires API-key authentication only.

## Run instructions

### 1. List tickets

```bash
python - <<'PY'
from freshdesk_connector import FreshdeskConnector

connector = FreshdeskConnector.from_env()
print(connector.list_tickets(page=1, per_page=30))
PY
```

### 2. Get ticket details

```bash
python - <<'PY'
from freshdesk_connector import FreshdeskConnector

connector = FreshdeskConnector.from_env()
print(connector.get_ticket(123))
PY
```

### 3. Search tickets

```bash
python - <<'PY'
from freshdesk_connector import FreshdeskConnector

connector = FreshdeskConnector.from_env()
print(connector.search_tickets("payment issue"))
PY
```

## Assumptions and limitations

- API key authentication is used instead of OAuth.
- Freshdesk ticket access is read-only; there are no create, update, or delete flows.
- Rate limits are handled with retry/backoff for HTTP 429 responses.
- The connector is scoped to Freshdesk ticket data only and does not expose user identities or unrelated fields.

## Rate-limit handling

Freshdesk trial accounts are commonly limited to roughly 50 requests per minute. The connector retries on HTTP 429 with exponential backoff and respects a `Retry-After` value when present.
