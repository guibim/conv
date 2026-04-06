from pathlib import Path
import shutil

from fastapi import UploadFile

from app.errors import InvalidInputError, PayloadTooLargeError


CHUNK_SIZE = 1024 * 1024


def ensure_matching_extension(filename: str | None, expected_format: str) -> str:
    if not filename:
        raise InvalidInputError("Uploaded file must include a filename.")

    suffix = Path(filename).suffix.lower().lstrip(".")
    if suffix != expected_format.lower():
        raise InvalidInputError(
            "Uploaded file extension does not match the declared source format."
        )

    return filename


async def save_upload_to_path(
    upload: UploadFile,
    destination: Path,
    max_upload_bytes: int,
) -> int:
    total_bytes = 0

    with destination.open("wb") as output_file:
        while True:
            chunk = await upload.read(CHUNK_SIZE)
            if not chunk:
                break

            total_bytes += len(chunk)
            if total_bytes > max_upload_bytes:
                raise PayloadTooLargeError(
                    f"File exceeds the maximum allowed size of {max_upload_bytes} bytes."
                )

            output_file.write(chunk)

    return total_bytes


def cleanup_temp_dir(temp_dir: str) -> None:
    shutil.rmtree(temp_dir, ignore_errors=True)
