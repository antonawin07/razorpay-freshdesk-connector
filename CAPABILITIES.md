# Freshdesk Connector Capabilities

## CAN DO
- List tickets from Freshdesk.
- Get ticket details by ticket ID.
- Search tickets by keyword.

## CANNOT DO
- Create, update, or delete tickets.
- Access user PII beyond the ticket fields returned by the Freshdesk API.
- Handle webhooks or event-driven integrations.
- Use OAuth. Freshdesk direct API access for this scope is API-key based Basic Auth, so OAuth is not supported here.

## Scope and limitations
- Authentication uses Basic Auth with the Freshdesk API key as the username and X as the password.
- This connector is read-only by design.
- Trial accounts are limited to approximately 50 requests per minute; HTTP 429 responses are retried with exponential backoff.
- No customer data, passwords, or credentials are stored in the codebase.
