# Contexto Master - Conv

## Overview

Conv is a lightweight file conversion platform organized as a QA-oriented technical project. It combines public APIs, data-format interoperability, deploy-time constraints, refactoring work, and validation assets in a single repository.

This file is intended to serve as the operational and technical master context for anyone maintaining, extending, testing, or deploying the project.

## Active Runtime Surfaces

### 1. Main API v2

- folder: [`api-v2`](api-v2)
- production URL: [https://conv-nyst.onrender.com](https://conv-nyst.onrender.com)
- role: new primary backend baseline

Main endpoints:

- `GET /`
- `GET /health`
- `GET /conversions`
- `POST /convert`

Key implementation files:

- [`api-v2/app/main.py`](api-v2/app/main.py)
- [`api-v2/app/routes/convert.py`](api-v2/app/routes/convert.py)
- [`api-v2/app/registry.py`](api-v2/app/registry.py)

### 2. Legacy API

- folder: [`app`](app)
- live URL: [https://conv-api-la6e.onrender.com](https://conv-api-la6e.onrender.com)
- role: historical implementation and legacy runtime

This code should not be treated as the long-term primary backend.

### 3. Metadata Extraction API

- folder: [`extract-img-api`](extract-img-api)
- live URL: [https://conv-yw21.onrender.com](https://conv-yw21.onrender.com)
- role: secondary API for image metadata extraction

### 4. Frontend

- live URL: [https://guibim.github.io/conv-site](https://guibim.github.io/conv-site)
- hosted separately from this repository
- current verification source: published bundle, not source code in-repo

## Stacks and Tooling

### Backend stack

- Python
- FastAPI
- Uvicorn
- python-multipart

### Parsing and format tooling

- defusedxml
- pyreadstat
- Pillow
- ExifRead

### Deployment and validation stack

- Render Free Tier
- Postman
- GitHub
- GitHub Pages

### Referenced external stack

- Lovable.dev
- browser `fetch`-based upload/download flow

## Why the Project Is Relevant for QA

Conv is a useful QA-oriented project because it concentrates several quality concerns in a small but realistic system:

- API contract validation
- input validation under public upload endpoints
- data-format compatibility behavior
- malformed payload handling
- encoding robustness
- reliability under free-tier deployment constraints
- documentation drift detection
- mismatch detection between frontend messaging and backend runtime reality

## Render Hosting Model

The project is hosted on **Render Free Tier**.

This matters because:

- the API can enter suspended state after inactivity
- the first request after idle time can take longer due to **cold start**
- dependency support is narrower than in more permissive environments
- infrastructure can directly determine which conversion formats are feasible

Cold start should therefore be explicitly documented in product-facing and technical-facing materials.

## Main API v2 Design

The `api-v2` backend was created to replace the older API shape with a safer and more maintainable baseline.

Core design principles:

- single conversion contract
- explicit conversion registry
- safer upload handling
- bounded input size
- temp file cleanup
- hardened XML parsing
- better separation between routing and conversion logic

### Configuration

Relevant variables:

- `ALLOWED_ORIGINS`
- `MAX_UPLOAD_BYTES`
- `CORS_ALLOW_CREDENTIALS`

Current default posture:

- restricted origin list
- credentials disabled by default
- 10 MB upload cap unless explicitly changed

## API v2 Conversion Matrix

Current registered conversions:

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

Current registry source:

- [`api-v2/app/registry.py`](api-v2/app/registry.py)

## Formats Not Yet Promoted into API v2

The repository still contains older or experimental implementations outside the current `api-v2` production contract.

Examples:

- `dta`
- `xlsx`
- `markdown`
- `yaml`
- `sql`
- `ifc` summary/export flows

These should not be considered active production capabilities of `api-v2` unless explicitly added to the new registry and validated.

## How to Run the Main API v2 Locally

From the repository root:

```bash
cd api-v2
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Useful local URLs:

- `http://localhost:8000/`
- `http://localhost:8000/health`
- `http://localhost:8000/conversions`
- `http://localhost:8000/docs`

## How to Deploy API v2 on Render

Use the same GitHub repository with:

- Branch: `master`
- Root Directory: `api-v2`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Recommended environment variables:

- `ALLOWED_ORIGINS=https://guibim.github.io`
- `MAX_UPLOAD_BYTES=10485760`
- `CORS_ALLOW_CREDENTIALS=false`

## Validation Assets

Validation-oriented repository assets:

- [`postman/conv-api-collection.json`](postman/conv-api-collection.json)
- [`postman/conv-api-environment.json`](postman/conv-api-environment.json)
- [`postman/readme.md`](postman/readme.md)

These are useful for:

- smoke testing
- response validation
- endpoint contract checks
- lightweight regression coverage

## Security and Reliability Notes

The repository contains historical risks in the legacy implementation, including:

- broken imports in the legacy conversion router
- unbounded temporary file accumulation
- unsafe XML parsing in older modules
- over-permissive CORS defaults in the old API

The `api-v2` implementation was created specifically to improve this baseline.

## Frontend Status and Inconsistencies

The published frontend is currently not fully aligned with the `api-v2` runtime.

Observed inconsistencies from published artifact inspection:

- frontend branding still presents the product as `Conv+` rather than the newer repository-level naming `Conv`
- frontend route inventory is broader than the active `api-v2` conversion registry
- frontend About page still describes older architecture and broader capabilities
- some public-facing messaging still implies support for formats not currently exposed by `api-v2`
- frontend still references the secondary metadata API directly as part of user-facing flow

Important limitation:

- frontend source code was not available in this repository
- verification was performed through the live HTML and downloaded bundle artifacts only

## Refactoring References

Primary refactoring documentation:

- [`docs/refatoracao-conversoes.md`](docs/refatoracao-conversoes.md)

This should be used together with `api-v2` as the current architectural baseline.

## Recommended Maintenance Direction

Short-term priorities:

1. use `api-v2` as the main supported backend
2. align the frontend with the `api-v2` conversion registry
3. keep documentation synchronized with runtime behavior
4. expose only conversions that are operationally stable under Render Free Tier
5. continue phasing out legacy assumptions from the public product narrative
