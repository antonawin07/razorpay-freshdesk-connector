from unittest.mock import patch

import pytest
import responses

from src.connector import FreshdeskConnector


@pytest.fixture
def connector() -> FreshdeskConnector:
    return FreshdeskConnector(domain="https://example.freshdesk.com", api_key="test_api_key")


@responses.activate
def test_list_tickets_returns_json(connector: FreshdeskConnector) -> None:
    responses.add(
        responses.GET,
        "https://example.freshdesk.com/api/v2/tickets",
        json=[{"id": 101, "subject": "First ticket"}],
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )

    result = connector.list_tickets(page=1)

    assert result[0]["id"] == 101


@responses.activate
def test_get_ticket_returns_json(connector: FreshdeskConnector) -> None:
    responses.add(
        responses.GET,
        "https://example.freshdesk.com/api/v2/tickets/42",
        json={"id": 42, "subject": "Issue"},
        status=200,
    )

    result = connector.get_ticket(42)

    assert result["id"] == 42
    assert result["subject"] == "Issue"


@responses.activate
def test_search_tickets_returns_json(connector: FreshdeskConnector) -> None:
    responses.add(
        responses.GET,
        "https://example.freshdesk.com/api/v2/search/tickets",
        json=[{"id": 7, "subject": "Payment issue"}],
        status=200,
        match=[responses.matchers.query_param_matcher({"query": "payment"})],
    )

    result = connector.search_tickets("payment")

    assert result[0]["id"] == 7


@responses.activate
def test_rate_limit_retries_successfully(connector: FreshdeskConnector) -> None:
    responses.add(
        responses.GET,
        "https://example.freshdesk.com/api/v2/tickets",
        status=429,
        body="rate limited",
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )
    responses.add(
        responses.GET,
        "https://example.freshdesk.com/api/v2/tickets",
        json=[{"id": 900, "subject": "Retry success"}],
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )

    with patch("src.connector.time.sleep", return_value=None) as sleep_mock:
        result = connector.list_tickets(page=1)

    assert result[0]["id"] == 900
    assert sleep_mock.called
