# Conv+ ⚙️  
A lightweight, web-based file conversion service.

🔗 Web application: https://guibim.github.io/conv-site
🖥️ Public API: https://conv-api-la6e.onrender.com
🖥️ Public API-2 (Metadata Extract): https://conv-yw21.onrender.com

---

## 🧠 Project Overview

**Conv+** is a minimalist online file conversion tool designed to simplify common data format transformations.

From a user perspective, Conv+ allows files to be uploaded through a web interface and converted into other formats in a fast and accessible way.  
From a technical perspective, the project serves as a **learning and experimentation platform** focused on modern backend APIs, deployment constraints, and client–server integration.

The project was created to explore and validate concepts such as:

- API development with **FastAPI**
- Deployment on constrained environments (Render free tier)
- Frontend–backend integration using **Lovable.dev**
- Browser-based file uploads and downloads
- Simple, accessible UX with minimal user friction

Conv+ is **actively evolving**, and new features and improvements are introduced incrementally.

---

## 🚀 Supported Conversions

The following conversions are currently supported through the `/convert` API endpoint:

| Conversion | Description |
|-----------|-------------|
| **DTA → CSV** | Converts Stata `.dta` files into CSV format |
| **TXT → CSV** | Converts plain text lines into a CSV column |
| **CSV → TXT** | Exports CSV data as a formatted text file |
| **CSV → JSON** | Converts tabular CSV data into structured JSON |
| **JSON → CSV** | Converts a JSON list into a CSV table |
| **CSV → XML** | Transforms CSV data into a hierarchical XML structure |
| **XML → CSV** | Flattens repetitive XML elements into CSV format |
| **CSV → HTML** | Generates an HTML table from CSV data |
| **HTML → TXT** | Extracts readable text content from an HTML file |
| **TXT → JSON** | Converts each line of a TXT file into a JSON array item |
| **JSON → TXT** | Converts a JSON array into a TXT file (one item per line) |

---

## ⚠️ CSV → DTA (Temporarily Disabled)

The **CSV → DTA** conversion was designed, implemented, and validated during development but is currently **disabled** due to infrastructure limitations.

### 📌 Technical Explanation

Generating `.dta` files requires the `pyreadstat` library, which in turn **strictly depends on a fully-featured pandas DataFrame**. The library does not accept alternative data structures or partial implementations.

However:

- The **Render free tier does not support installing pandas**, as it depends on native system libraries (C extensions, OpenBLAS, libgcc, etc.)
- The execution environment **does not allow compiling these dependencies**
- Lightweight alternatives (e.g., `pandas-lite`) are insufficient because they **do not implement the internal structures required by the `.dta` format**
- As a result, attempts to generate `.dta` files consistently fail with a `500 Internal Server Error`

> **Conclusion:**  
> The `CSV → DTA` conversion cannot be reliably supported in the current hosting environment.  
> This feature may be re-enabled if the backend is migrated to an environment with full pandas support (e.g., Railway, Fly.io, Google Cloud Run).

---

## 🧊 Cold Start Behavior

The backend API is hosted on a free-tier platform, which introduces a **cold start behavior**:

- After a period of inactivity, the server enters a suspended state
- The first request after suspension may take **20–60 seconds** to complete while the server initializes
- Subsequent requests are processed normally with low latency

This behavior is communicated to users directly in the frontend to avoid confusion during conversions.

---

## 🧱 Technical Architecture

### **Frontend**
- Built with **Lovable.dev**
- Lightweight, responsive, and minimal UI
- Files are uploaded directly from the browser
- Communication with the backend via standard HTTP requests (`fetch`)

### **Backend**
- **Python + FastAPI**
- Hosted on Render (Free Tier)
- Core endpoint:
  - `POST /convert`

### **Core Dependencies**
- `fastapi`
- `uvicorn`
- `python-multipart`
- `pyreadstat` (read-only support for `.dta` files)

### **Planned Improvements**
- Re-enable CSV → DTA in a supported environment
- PDF ↔ Image conversions
- Additional data formats (XLSX, JSON, Parquet)
- Conversion history and persistence using Supabase

---

## 📡 API Usage

### **Endpoint**
### **Request Parameters**
- `file` — input file
- `from_format` — source format
- `to_format` — target format

### **Response**
The converted file, returned directly and ready for download.

---

## 🧪 Project Status

> **Conv+ is an educational and experimental project under continuous refinement.**  
> Its primary goal is learning and validation of technical concepts, and changes may occur frequently.

Feedback and contributions are welcome.

---

## 👤 Author

Developed by:

- GitHub: https://github.com/guibim  
- LinkedIn: https://www.linkedin.com/in/guilherme-bim

---

