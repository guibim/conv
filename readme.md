# Conv

Conv is a file conversion platform built as a lightweight web service and as a QA-oriented engineering project. The repository combines file transformation workflows, API design, deployment constraints, validation assets, and refactoring work across multiple runtime surfaces.

The project is intentionally relevant from a quality engineering perspective: it deals with imperfect inputs, encoding variability, conversion consistency, deploy-time limitations, and public-facing API behavior under constrained infrastructure.

## Current Public Endpoints

- Web application: [https://guibim.github.io/conv-site](https://guibim.github.io/conv-site)
- Main API v2: [https://conv-nyst.onrender.com](https://conv-nyst.onrender.com)
- Legacy conversion API: [https://conv-api-la6e.onrender.com](https://conv-api-la6e.onrender.com)
- Image metadata API: [https://conv-yw21.onrender.com](https://conv-yw21.onrender.com)

Operational note:

- the active frontend now targets `api-v2` for both conversion and image metadata extraction
- the legacy APIs remain online as historical or transitional surfaces, not as the preferred public contract

## Repository Scope

This repository currently contains five relevant areas:

1. Legacy conversion backend in [`app`](app)
2. New hardened conversion backend in [`api-v2`](api-v2)
3. Independent image metadata extraction API in [`extract-img-api`](extract-img-api)
4. API validation assets in [`postman`](postman)
5. Refactoring and architecture material in [`docs`](docs)

The frontend is maintained in a separate repository:

- frontend source: [https://github.com/guibim/conv-site](https://github.com/guibim/conv-site)
- published frontend: [https://guibim.github.io/conv-site](https://guibim.github.io/conv-site)

## Architecture Overview

### `api-v2`

The new production-oriented backend lives in [`api-v2`](api-v2). This is the API that should be used as the main baseline for ongoing work.

Core characteristics:

- FastAPI-based HTTP service
- explicit conversion registry
- normalized conversion contract
- upload size limits
- cleanup of temporary artifacts
- hardened XML parsing with `defusedxml`
- safer HTML generation for `csv -> html`
- operationally safer defaults for CORS and error handling

Key files:

- entrypoint: [`api-v2/app/main.py`](api-v2/app/main.py)
- routes: [`api-v2/app/routes/convert.py`](api-v2/app/routes/convert.py)
- registry: [`api-v2/app/registry.py`](api-v2/app/registry.py)
- converters: [`api-v2/app/converters`](api-v2/app/converters)

### Legacy backend

The original backend remains in [`app`](app) as legacy implementation and historical reference. It should not be treated as the primary architectural baseline going forward.

### Image metadata API

The EXIF-focused service remains separate in [`extract-img-api`](extract-img-api). It should now be treated as a legacy or transitional surface, because equivalent image metadata extraction capability has been incorporated into `api-v2`.

### Frontend

The frontend has already been refactored in the separate `conv-site` repository to align with the current `api-v2` contract.

Current frontend posture:

- `Conv` branding aligned with the repository and backend naming
- only active `api-v2` conversion routes are exposed in the public catalog
- `POST /extract-metadata` from `api-v2` is used as the main metadata flow
- frontend copy explicitly mentions Render Free Tier and cold start behavior
- older conversion flows such as `dta`, `xlsx`, `sql`, `markdown`, `yaml`, and IFC-related routes are no longer presented as active production capabilities

## Main API v2 Endpoints

The new API exposes:

- `GET /`
- `GET /health`
- `GET /conversions`
- `POST /convert`
- `POST /extract-metadata`

Example request model for `POST /convert`:

- `file`: uploaded file
- `from_format`: declared source format
- `to_format`: declared target format

The response is the converted file returned directly as a downloadable artifact.

The same API also supports structured image metadata extraction through `POST /extract-metadata`.

Current metadata extraction output includes:

- file information
- file hashes
- content type
- image dimensions
- image mode and format
- animation and frame hints when available
- Pillow-derived EXIF metadata
- ExifRead-derived EXIF and maker-note style metadata
- GPS coordinates when present
- diagnostics and extraction warnings

## Current API v2 Conversion Coverage

The current `api-v2` registry includes:

- `txt -> csv`
- `csv -> txt`
- `csv -> json`
- `json -> csv`
- `csv -> xml`
- `xml -> csv`
- `csv -> html`
- `html -> txt`
- `txt -> json`
- `json -> txt`
- `txt -> xml`
- `json -> xml`
- `xml -> json`

The live list can also be queried directly from:

- [https://conv-nyst.onrender.com/conversions](https://conv-nyst.onrender.com/conversions)

The frontend catalog should be treated as a UI reflection of this registry, not as an independent source of truth.

## Quality Engineering Positioning

Conv is useful as a QA-facing project because it exercises several system-quality concerns at once:

- multipart API contract validation
- source and target format compatibility checks
- file extension and declared format alignment
- text decoding under multiple encodings
- malformed payload handling
- regression risk when introducing new converters
- infrastructure-aware reliability decisions
- public API behavior under constrained hosting

This is not just a format conversion demo. It is a compact platform for validating technical correctness under realistic API and deployment conditions.

## Deployment Model

The project is hosted on **Render Free Tier**. This has direct impact on both user experience and technical design.

Operational implications:

- the service may experience **cold start** after inactivity
- the first request may take noticeably longer than subsequent ones
- dependency choices must remain compatible with free-tier runtime constraints
- some format pairs cannot be safely exposed under the current environment

This cold start behavior should be considered expected platform behavior, not an application defect by itself.

## Render Setup for `api-v2`

The new API is designed to be deployed from this same repository using:

- Branch: `master`
- Root Directory: `api-v2`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Recommended environment variables:

- `ALLOWED_ORIGINS=https://guibim.github.io`
- `MAX_UPLOAD_BYTES=10485760`
- `CORS_ALLOW_CREDENTIALS=false`

## Technical Stacks

Primary technologies currently present in the repository:

- Python
- FastAPI
- Uvicorn
- python-multipart
- defusedxml
- pyreadstat
- Pillow
- ExifRead
- Postman
- Render

Adjacent or externally referenced stack components:

- Lovable.dev
- browser-based upload/download flows via `fetch`
- GitHub Pages for frontend hosting

## Current Refactoring Material

The repository already includes dedicated refactoring guidance in:

- [`docs/refatoracao-conversoes.md`](docs/refatoracao-conversoes.md)

This document captures the standardization plan for conversion contracts, registry structure, migration strategy, and classification of stable versus problematic formats.

## Frontend Alignment Status

The frontend source is now known and has been updated in its own repository to reflect the current backend reality.

Current frontend alignment decisions:

- use `api-v2` as the main integration target
- expose only supported conversion routes from the current production contract
- keep image metadata extraction in the same main user flow
- present Render Free Tier and cold start as expected runtime characteristics

Remaining documentation caveat:

- this repository still does not contain the frontend source itself, so frontend implementation changes happen in the separate `conv-site` repository

## Documentation Companion

For a more complete technical reference, see:

- [`contexto_master.md`](contexto_master.md)

That file centralizes the master context of the project, active stacks, deployment model, current APIs, and practical usage notes.

## Engineering Status

The project is active and under structured refactoring.

The current technical direction is:

- keep the runtime lightweight
- align documentation with runtime reality
- use `api-v2` as the new primary backend baseline
- keep the frontend aligned with the `api-v2` registry and metadata endpoint
- reduce security and availability risks present in the legacy API
- improve testability and operational clarity

## Author

- GitHub: [guibim](https://github.com/guibim)
- LinkedIn: [Guilherme Bim](https://www.linkedin.com/in/guilherme-bim)
