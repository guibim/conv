from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import exifread
from PIL import Image, ExifTags
import tempfile
import os

app = FastAPI(
    title="Image Metadata Extractor API",
    version="1.1.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}


def extract_with_pillow(path: str) -> dict:
    data = {}
    try:
        img = Image.open(path)
        exif = img._getexif()
        if exif:
            for tag, value in exif.items():
                name = ExifTags.TAGS.get(tag, tag)
                data[f"PIL:{name}"] = str(value)
    except Exception:
        pass
    return data


def extract_with_exifread(path: str) -> dict:
    data = {}
    with open(path, "rb") as f:
        tags = exifread.process_file(
            f,
            details=True,
            strict=False
        )
    for k, v in tags.items():
        data[f"EXIF:{k}"] = str(v)
    return data


@app.post("/extract-exif")
async def extract_exif(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = {
            "filename": file.filename,
            "content_type": file.content_type,
            "metadata": {}
        }

        # Pillow (EXIF padrão)
        result["metadata"].update(extract_with_pillow(tmp_path))

        # ExifRead (EXIF + MakerNotes)
        result["metadata"].update(extract_with_exifread(tmp_path))

        os.remove(tmp_path)

        if not result["metadata"]:
            return JSONResponse(
                content={"message": "No metadata found"},
                status_code=200
            )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
