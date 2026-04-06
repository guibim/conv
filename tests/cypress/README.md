# Cypress Test Planning

This folder is a Cypress-oriented planning space.

The current content is documentary only. It is written to make future automation straightforward once the frontend and backend contracts stabilize.

## Intent

Use Cypress as the preferred end-to-end layer for:

- browser flow validation
- upload/download interaction coverage
- frontend/backend consistency checks
- smoke and regression testing against deployed environments

## Suggested Future Automation Scope

### API-backed UI flows

- selecting a conversion type
- uploading a file
- submitting conversion
- receiving downloadable output
- displaying controlled error states

### Informational validation

- cold start warning visibility
- supported format inventory
- metadata extraction messaging
- About page consistency with actual architecture

### Operational validation

- deployed environment health checks
- cross-checking frontend options against `/conversions`

## Suggested Future Command Model

Possible future commands:

```bash
npx cypress open
npx cypress run
```

Possible future environment targets:

- local `api-v2`
- deployed `conv-nyst`
- published frontend on GitHub Pages

## Scenario Organization

Scenarios are currently grouped into:

- `00-smoke`
- `01-core-conversions`
- `02-validation-and-errors`
- `03-metadata`
- `04-runtime-and-render`
- `05-frontend-consistency`

Each scenario file uses Gherkin-style BDD so it can later be translated into Cypress specs if desired.
