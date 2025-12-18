from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import exifread
import tempfile
import os

app = FastAPI(
    title="Image EXIF Extractor API",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract-exif")
async def extract_exif(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            tags = exifread.process_file(f, details=False)

        os.remove(tmp_path)

        if not tags:
            return JSONResponse(
                content={"message": "No EXIF metadata found"},
                status_code=200
            )

        return {
            "filename": file.filename,
            "exif": {k: str(v) for k, v in tags.items()}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
