from pathlib import Path
import tempfile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from app.config import settings
from app.errors import ConversionError, UnsupportedConversionError
from app.models import ConversionContext
from app.registry import get_conversion, list_conversions
from app.utils.uploads import cleanup_temp_dir, ensure_matching_extension, save_upload_to_path


router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.service_name, "version": settings.version}


@router.get("/conversions")
def conversions() -> dict[str, object]:
    return {
        "count": len(list_conversions()),
        "items": list_conversions(),
    }


@router.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    from_format: str = Form(...),
    to_format: str = Form(...),
):
    source_format = from_format.lower().strip()
    target_format = to_format.lower().strip()

    spec = get_conversion(source_format, target_format)
    if spec is None:
        raise HTTPException(
            status_code=UnsupportedConversionError.status_code,
            detail=f"Unsupported conversion: {source_format} -> {target_format}.",
        )

    filename = ensure_matching_extension(file.filename, source_format)
    temp_dir = tempfile.mkdtemp(prefix="conv-api-v2-")

    try:
        input_path = Path(temp_dir) / f"input.{source_format}"
        await save_upload_to_path(file, input_path, settings.max_upload_bytes)
        payload = input_path.read_bytes()

        result = spec.handler(
            payload,
            ConversionContext(
                source_format=source_format,
                target_format=target_format,
                filename=filename,
            ),
        )

        original_stem = Path(filename).stem or "converted"
        output_name = f"{original_stem}.{result.extension}"
        output_path = Path(temp_dir) / output_name
        output_path.write_bytes(result.output_bytes)

        headers = {}
        if result.warnings:
            headers["X-Conv-Warnings"] = " | ".join(result.warnings)

        return FileResponse(
            path=output_path,
            media_type=result.media_type,
            filename=output_name,
            headers=headers,
            background=BackgroundTask(cleanup_temp_dir, temp_dir),
        )

    except ConversionError as error:
        cleanup_temp_dir(temp_dir)
        raise HTTPException(status_code=error.status_code, detail=error.message) from error
    except Exception:
        cleanup_temp_dir(temp_dir)
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error while processing the conversion.",
        )
    finally:
        await file.close()
