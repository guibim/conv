# Conv+ API – Postman Collection

Postman collection covering the happy path for all supported file conversions
using the `/convert` endpoint.

## Endpoint
POST /convert (multipart/form-data)

## Parameters
- file
- from_format
- to_format

## Scope
- Smoke test
- Happy path conversions
- Status, response time and body validation

## Known Limitation
- CSV files must be UTF-8 encoded (see roadmap for 1.0v)

## Usage
Import the collection and environment into Postman and run via Collection Runner.
