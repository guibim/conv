# Tests - Strategy and Structure

This directory is the documentation-first testing area for the Conv project.

It is intentionally organized to support a future Cypress-based workflow, but it is currently documentation-only. The goal is to define coverage, scenarios, and BDD narratives before binding tests to implementation.

## Objectives

- centralize QA coverage planning
- document expected user-facing and API-facing behaviors
- define smoke, regression, validation, and environment scenarios
- keep frontend and backend expectations aligned
- support a future Cypress E2E suite without blocking current refactoring work

## Scope

This `tests/` area currently covers:

- conversion flow smoke scenarios
- input validation scenarios
- error handling and unsupported conversion scenarios
- metadata extraction scenarios
- Render Free Tier operational behavior
- high-level frontend/backend consistency checks

## Current Status

This area is:

- documentation-first
- not wired into CI
- not bound to runtime code
- intended as the canonical testing plan for future Cypress adoption

## Suggested Future Layout

```text
tests/
  README.md
  test-matrix.md
  cypress/
    README.md
    e2e/
      00-smoke/
      01-core-conversions/
      02-validation-and-errors/
      03-metadata/
      04-runtime-and-render/
      05-frontend-consistency/
    fixtures/
    reports/
```

## Test Layers

### 1. Smoke

Purpose:

- verify service availability
- confirm main routes respond
- validate essential happy-path flows

### 2. Functional conversion validation

Purpose:

- verify supported conversion mappings
- validate file output type and structure
- detect regressions in conversion logic

### 3. Negative-path validation

Purpose:

- validate unsupported format combinations
- validate bad payloads
- validate extension mismatch handling
- validate malformed JSON, XML, and HTML inputs

### 4. Operational and environment validation

Purpose:

- verify cold start messaging and resilience
- verify frontend/backend alignment
- verify Render-hosted deployment expectations

## Living Documents

Primary documents in this directory:

- [`test-matrix.md`](test-matrix.md)
- [`cypress/README.md`](cypress/README.md)

BDD scenarios are documented under:

- [`cypress/e2e`](cypress/e2e)

## Usage Guidance

For now, this directory should be used to:

- define new scenarios before implementation
- record expected business behavior
- guide manual QA and exploratory testing
- serve as a blueprint for future Cypress automation
