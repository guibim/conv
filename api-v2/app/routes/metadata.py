from pathlib import Path
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.errors import ConversionError
from app.metadata import extract_image_metadata
from app.utils.uploads import cleanup_temp_dir, save_upload_to_path


router = APIRouter()


@router.post("/extract-metadata")
async def extract_metadata(file: UploadFile = File(...)) -> dict[str, object]:
    temp_dir = tempfile.mkdtemp(prefix="conv-api-v2-metadata-")

    try:
        suffix = Path(file.filename or "upload.bin").suffix or ".bin"
        input_path = Path(temp_dir) / f"input{suffix}"
        await save_upload_to_path(file, input_path, settings.max_upload_bytes)
        payload = input_path.read_bytes()

        return extract_image_metadata(
            payload=payload,
            image_path=input_path,
            filename=file.filename or input_path.name,
            content_type=file.content_type,
        )

    except ConversionError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from error
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error while extracting image metadata.",
        )
    finally:
        cleanup_temp_dir(temp_dir)
        await file.close()
