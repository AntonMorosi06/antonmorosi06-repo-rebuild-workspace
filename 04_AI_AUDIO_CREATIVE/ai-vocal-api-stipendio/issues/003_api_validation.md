# Issue 003 - API validation

## Goal

Improve input validation and error messages.

## Current implementation

Pydantic validates numeric ranges for predict requests. The service returns additional warnings for unusual values.

## Future improvements

Add richer validation messages.

Add request examples to OpenAPI metadata.

Add API tests with TestClient.

Add structured error response schemas.
