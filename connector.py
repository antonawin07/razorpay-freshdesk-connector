"""Freshdesk connector for read-only ticket access."""

from __future__ import annotations

import time
from typing import Any

import requests
from requests.auth import HTTPBasicAuth


class FreshdeskConnector:
    """Simple read-only Freshdesk connector for AI agent ticket access."""

    def __init__(self, domain: str, api_key: str) -> None:
        """Initialize a Freshdesk connector with Basic Auth credentials.

        Args:
            domain: Freshdesk domain URL, for example https://company.freshdesk.com.
            api_key: Freshdesk API key used as the Basic Auth username.
        """
        if not domain:
            raise ValueError("Freshdesk domain cannot be empty.")
        if not api_key:
            raise ValueError("Freshdesk API key cannot be empty.")

        self.domain: str = domain.rstrip("/")
        self.session: requests.Session = requests.Session()
        self.session.auth = HTTPBasicAuth(api_key, "X")

    def _request(self, method: str, url: str, **kwargs: Any) -> Any:
        """Send an authenticated HTTP request with 429 retry backoff.

        Args:
            method: HTTP method to use.
            url: Full URL to request.
            **kwargs: Additional requests arguments such as params.

        Returns:
            The decoded JSON payload if the response contains JSON.

        Raises:
            RuntimeError: If the request fails or rate-limit retries are exhausted.
        """
        for attempt in range(3):
            response = self.session.request(method=method, url=url, **kwargs)

            if response.status_code == 429:
                if attempt == 2:
                    raise RuntimeError("Freshdesk rate limit exceeded after 3 retries.")
                sleep_for = [1, 2, 4][attempt]
                time.sleep(sleep_for)
                continue

            if response.ok:
                if not response.content:
                    return {}
                return response.json()

            if response.status_code == 401:
                raise PermissionError("Freshdesk authentication failed. Check the API key and domain.")

            raise RuntimeError(
                f"Freshdesk request failed with status {response.status_code}: {response.text[:200]}"
            )

        raise RuntimeError("Freshdesk request failed without returning a valid response.")

    def list_tickets(self, page: int = 1) -> Any:
        """Return a paginated list of Freshdesk tickets.

        Args:
            page: The page number to request.

        Returns:
            JSON returned by the Freshdesk tickets endpoint.
        """
        url = f"{self.domain}/api/v2/tickets"
        return self._request("GET", url, params={"page": page})

    def get_ticket(self, ticket_id: int) -> Any:
        """Return a single Freshdesk ticket by id.

        Args:
            ticket_id: Ticket id to fetch.

        Returns:
            JSON returned by the Freshdesk ticket endpoint.
        """
        url = f"{self.domain}/api/v2/tickets/{ticket_id}"
        return self._request("GET", url)

    def search_tickets(self, query: str) -> Any:
        """Search Freshdesk tickets by keyword.

        Args:
            query: Search string to match against ticket content.

        Returns:
            JSON returned by the Freshdesk search endpoint.
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        url = f"{self.domain}/api/v2/search/tickets"
        return self._request("GET", url, params={"query": query})
