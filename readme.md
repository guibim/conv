# Conv

Conv is a file conversion platform designed as a lightweight web service and as a quality-oriented engineering project. It combines format transformation workflows, API integration, deployment constraints, and validation concerns in a single repository.

From a product perspective, the platform provides browser-based file conversion with minimal user friction. From an engineering perspective, the project is used to exercise API contract design, encoding robustness, negative-path handling, deployment behavior on free-tier infrastructure, and cross-stack integration between frontend and backend services.

## Project Positioning

This repository should be read as more than a simple converter demo.

It is a practical QA-focused project that touches multiple concerns:

- backend API design with FastAPI
- file parsing and transformation across heterogeneous formats
- browser-to-API integration
- constrained deployment environments on Render
- functional validation through Postman collections
- error handling around malformed files, unsupported mappings, and encoding issues
- secondary metadata extraction workflows for image files

The current direction of the project is to keep the runtime footprint small while improving technical consistency, observability, and reliability.

## Public Endpoints

- Web application: [https://guibim.github.io/conv-site](https://guibim.github.io/conv-site)
- Main conversion API: [https://conv-api-la6e.onrender.com](https://conv-api-la6e.onrender.com)
- Image metadata API: [https://conv-yw21.onrender.com](https://conv-yw21.onrender.com)

## Repository Scope

This repository currently contains four relevant areas:

1. Main conversion backend in [`app`](app)
2. Independent image metadata extraction API in [`extract-img-api`](extract-img-api)
3. API validation assets in [`postman`](postman)
4. Deployment descriptors such as [`render.yaml`](render.yaml) and [`render-build.sh`](render-build.sh)

The frontend is referenced by this project but is hosted separately.

## Architecture Overview

### Main conversion service

The primary service is implemented with FastAPI and exposes a conversion-oriented HTTP interface. The current application entry point is [`app/main.py`](app/main.py), and the main request flow is concentrated in [`app/routes/convert.py`](app/routes/convert.py).

Current responsibilities:

- receive multipart uploads
- validate source and target format pairing
- persist temporary input and output artifacts
- dispatch to a format-specific conversion handler
- return the converted file as a download response

### Image metadata extraction service

The repository also includes a secondary FastAPI service at [`extract-img-api/extract_img.py`](extract-img-api/extract_img.py). This component is intentionally separate from the main conversion API and focuses on metadata extraction from image uploads using Pillow and ExifRead.

### Cross-stack context

The project spans multiple layers even though they are not all implemented in this repository:

- frontend UX and file upload flow
- backend API behavior
- deployment/runtime constraints
- API contract validation tooling
- data-format interoperability

This cross-stack nature is one of the reasons the project is useful from a QA and systems-validation perspective.

## Quality Engineering Focus

Conv is particularly relevant as a QA-facing project because its value is not only in successful conversions, but also in predictable behavior under imperfect inputs and infrastructure constraints.

Key quality themes in this repository:

- contract validation for multipart API requests
- boundary checks for source and target format combinations
- verification of file extension and declared format alignment
- encoding tolerance for text-based formats such as CSV, TXT, HTML, and JSON
- handling of malformed or structurally incompatible content
- regression risk introduced by adding new converters incrementally
- operational behavior under Render cold starts

This makes the project a useful case study in functional QA, API QA, and reliability-focused refactoring.

## Current Supported Conversion Paths

The repository currently includes handlers for the following conversion families:

### Core text and tabular flows

- `dta -> csv`
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

### Additional implemented conversion modules

The codebase also contains modules for additional transformations and export-oriented outputs, including:

- `csv -> xlsx`
- `xlsx -> csv`
- `csv -> md`
- `html -> md`
- `json -> xml`
- `xml -> json`
- `json -> yaml`
- `csv -> sql`
- `ifc -> csv`
- `ifc -> json`
- `ifc -> html`
- `ifc -> txt`

Important note:

The repository is currently undergoing architectural standardization. Some newer conversion modules exist in code but are not yet fully normalized under a single execution contract. The refactoring plan for this standardization is documented in [`docs/refatoracao-conversoes.md`](docs/refatoracao-conversoes.md).

## Format Limitations and Technical Constraints

### CSV to DTA

`csv -> dta` is not a reliable public capability in the current hosting setup.

The implementation depends on `pyreadstat` and, in practice, on a fully compatible pandas-style DataFrame workflow. That requirement conflicts with the constraints of the current free-tier deployment model, where heavyweight native dependencies are difficult or impossible to support consistently.

For that reason, `csv -> dta` should be treated as infrastructure-blocked rather than production-ready.

### XML and HTML transformations

Some format pairs are intentionally simple and should not be interpreted as full semantic transformations.

- `xml -> csv` assumes repetitive, flattenable XML structures
- `html -> txt` is a lightweight text extraction path, not a browser-grade DOM rendering pipeline
- `html -> md` is a simplified conversion path with limited markup fidelity

### IFC exports

The IFC-related modules behave more like summary and reporting outputs than complete model conversions. They are useful for inspection and lightweight reporting, but they should not be presented as full BIM transformation pipelines.

## QA Assets in the Repository

The repository already contains validation-oriented assets in [`postman`](postman):

- Postman collection for `/convert`
- environment file for repeatable execution
- smoke-test oriented request coverage

These assets are particularly relevant from a QA standpoint because they provide a baseline for:

- endpoint contract verification
- response status validation
- response time monitoring
- happy-path regression checks

## Deployment and Runtime Considerations

The project is deployed on Render free tier infrastructure. This has direct quality implications and should be considered part of the system behavior, not an incidental detail.

Known operational characteristics:

- cold starts may delay the first request after inactivity
- infrastructure constraints affect dependency strategy
- deployment choices directly influence which conversions can be safely exposed

The current [`render.yaml`](render.yaml) is configured for the image metadata API, while the main conversion backend and public endpoints represent a broader project context.

## Technology Stack

Primary technologies currently visible in the repository:

- Python
- FastAPI
- Uvicorn
- python-multipart
- pyreadstat
- Pillow
- ExifRead
- Postman
- Render

Referenced or adjacent technologies in the broader project context:

- Lovable.dev for frontend generation/integration
- browser `fetch` workflows for upload/download handling

## Engineering Status

The project is active and under refactoring.

The current technical priority is not to add as many conversions as possible, but to improve the consistency of the conversion contract, the maintainability of the codebase, and the trustworthiness of the documented feature set.

That work includes:

- standardizing converter interfaces
- separating HTTP concerns from conversion logic
- classifying conversions by stability level
- improving documentation accuracy
- strengthening testability and regression coverage

The technical blueprint for that effort is available in [`docs/refatoracao-conversoes.md`](docs/refatoracao-conversoes.md).

## Why This Project Matters for QA

For a QA-oriented portfolio or technical narrative, Conv is useful because it shows interaction between business behavior and engineering constraints.

It demonstrates work around:

- API contract verification
- file-format compatibility analysis
- failure-mode documentation
- deployment-aware quality decisions
- data parsing under real-world encoding variance
- validation of user-facing behavior against backend limitations

In that sense, the project is not just a converter. It is a compact system for validating reliability across format handling, infrastructure limits, and integration surfaces.

## Author

- GitHub: [guibim](https://github.com/guibim)
- LinkedIn: [Guilherme Bim](https://www.linkedin.com/in/guilherme-bim)
