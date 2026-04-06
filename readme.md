# Conv

Conv is a file conversion platform built as a lightweight web service and as a QA-oriented engineering project. The repository combines file transformation workflows, API design, deployment constraints, validation assets, and refactoring work across multiple runtime surfaces.

The project is intentionally relevant from a quality engineering perspective: it deals with imperfect inputs, encoding variability, conversion consistency, deploy-time limitations, and public-facing API behavior under constrained infrastructure.

## Current Public Endpoints

- Web application: [https://guibim.github.io/conv-site](https://guibim.github.io/conv-site)
- Main API v2: [https://conv-nyst.onrender.com](https://conv-nyst.onrender.com)
- Legacy conversion API: [https://conv-api-la6e.onrender.com](https://conv-api-la6e.onrender.com)
- Image metadata API: [https://conv-yw21.onrender.com](https://conv-yw21.onrender.com)

## Repository Scope

This repository currently contains five relevant areas:

1. Legacy conversion backend in [`app`](app)
2. New hardened conversion backend in [`api-v2`](api-v2)
3. Independent image metadata extraction API in [`extract-img-api`](extract-img-api)
4. API validation assets in [`postman`](postman)
5. Refactoring and architecture material in [`docs`](docs)

The frontend is referenced by this repository but is hosted separately.

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

## Known Frontend Inconsistencies

The currently published frontend was checked against the live bundle and the current backend state. The following inconsistencies are visible today:

- the frontend still uses the older `Conv+` branding and title while the repository and new backend documentation now use `Conv`
- the frontend still references legacy conversion routes and capabilities that are broader than the `api-v2` registry
- the site still includes navigation for routes such as `dta -> csv`, `csv -> sql`, `csv -> markdown`, `html -> markdown`, `json -> yaml`, and IFC-related outputs, while these are not part of the current `api-v2` production contract
- the frontend metadata flow still points to the legacy image metadata API instead of the new `api-v2` metadata endpoint
- the About page text still describes the older modular service model and a broader set of use cases than the new hardened API currently exposes

Important limitation:

- frontend code was not available in this repository for direct code review
- the frontend verification was performed against the published application artifact and downloaded bundle, not its source repository

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
- reduce security and availability risks present in the legacy API
- improve testability and operational clarity

## Author

- GitHub: [guibim](https://github.com/guibim)
- LinkedIn: [Guilherme Bim](https://www.linkedin.com/in/guilherme-bim)
