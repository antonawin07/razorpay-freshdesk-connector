"""Simple demo script for the Freshdesk connector."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from connector import FreshdeskConnector  # noqa: E402


def main() -> None:
    """Load environment variables and list tickets from Freshdesk."""
    load_dotenv()

    domain = os.getenv("FRESHDESK_DOMAIN")
    api_key = os.getenv("FRESHDESK_API_KEY")

    if not domain or not api_key:
        print("Missing FRESHDESK_DOMAIN or FRESHDESK_API_KEY in environment.")
        return

    connector = FreshdeskConnector(domain=domain, api_key=api_key)

    try:
        tickets = connector.list_tickets(page=1)
        if isinstance(tickets, dict):
            results = tickets.get("results", tickets.get("tickets", []))
            count = len(results)
        elif isinstance(tickets, list):
            count = len(tickets)
        else:
            count = 0

        print(f"Tickets found: {count}")
    except PermissionError as exc:
        print(f"Authentication error: {exc}")
    except Exception as exc:  # pragma: no cover
        print(f"Error fetching tickets: {exc}")


if __name__ == "__main__":
    main()
