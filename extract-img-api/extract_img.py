from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import tempfile
import os

app = FastAPI(
    title="Conv+ Image Metadata API",
    description="Extract image metadata (EXIF, XMP, IPTC, GPS) using ExifTool",
    version="1.0.0"
)

# --------------------------------------------------
# CORS (ajuste depois para domínio específico)
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajustar futuramente
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Configurações
# --------------------------------------------------

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
EXIFTOOL_TIMEOUT = 10  # segundos

# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}

# --------------------------------------------------
# Endpoint principal
# --------------------------------------------------

@app.post("/image/metadata")
async def extract_image_metadata(file: UploadFile = File(...)):
    # Validação de tipo
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only image files are allowed."
        )

    # Leitura do arquivo
    contents = await file.read()

    # Validação de tamanho
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large. Maximum allowed size is 10MB."
        )

    # Arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # Execução do ExifTool
        result = subprocess.run(
            [
                "exiftool",
                "-j",
                "-G",
                "-n",
                "-a",
                "-u",
                "-ee",
                tmp_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=EXIFTOOL_TIMEOUT
        )

        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"ExifTool error: {result.stderr.strip()}"
            )

        metadata = json.loads(result.stdout)

        # ExifTool sempre retorna uma lista
        if not metadata or not isinstance(metadata, list):
            raise HTTPException(
                status_code=500,
                detail="Failed to parse metadata output."
            )

        return metadata[0]

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=504,
            detail="Metadata extraction timed out."
        )

    finally:
        # Limpeza obrigatória
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
