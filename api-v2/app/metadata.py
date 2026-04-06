from fractions import Fraction
import hashlib
from pathlib import Path

import exifread
from PIL import ExifTags, Image

from app.errors import InvalidInputError


def _stringify(value) -> str:
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8", errors="replace")
        except Exception:
            return repr(value)
    return str(value)


def _ratio_to_float(value):
    if hasattr(value, "num") and hasattr(value, "den"):
        denominator = value.den or 1
        return float(value.num) / float(denominator)

    if isinstance(value, Fraction):
        return float(value)

    if isinstance(value, tuple) and len(value) == 2:
        numerator, denominator = value
        denominator = denominator or 1
        return float(numerator) / float(denominator)

    return float(value)


def _gps_coordinate(values, ref: str | None) -> float | None:
    if not values or len(values) < 3:
        return None

    degrees = _ratio_to_float(values[0])
    minutes = _ratio_to_float(values[1])
    seconds = _ratio_to_float(values[2])

    coordinate = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in {"S", "W"}:
        coordinate *= -1
    return round(coordinate, 8)


def _extract_pillow_metadata(image_path: Path) -> tuple[dict[str, str], dict[str, object]]:
    metadata: dict[str, str] = {}
    image_info: dict[str, object] = {}
    gps: dict[str, object] = {}

    with Image.open(image_path) as image:
        image_info.update(
            {
                "format": image.format,
                "mode": image.mode,
                "width": image.width,
                "height": image.height,
                "is_animated": bool(getattr(image, "is_animated", False)),
                "frame_count": int(getattr(image, "n_frames", 1)),
                "has_transparency": "transparency" in image.info
                or image.mode in {"RGBA", "LA"},
                "info_keys": sorted(image.info.keys()),
                "icc_profile_present": "icc_profile" in image.info,
            }
        )

        dpi = image.info.get("dpi")
        if dpi:
            image_info["dpi"] = list(dpi) if isinstance(dpi, tuple) else dpi

        exif = image.getexif()
        if exif:
            for tag, value in exif.items():
                tag_name = ExifTags.TAGS.get(tag, str(tag))
                metadata[tag_name] = _stringify(value)

            gps_info = exif.get_ifd(34853) if 34853 in exif else None
            if gps_info:
                gps_data = {
                    ExifTags.GPSTAGS.get(tag, str(tag)): value
                    for tag, value in gps_info.items()
                }
                latitude = _gps_coordinate(
                    gps_data.get("GPSLatitude"), gps_data.get("GPSLatitudeRef")
                )
                longitude = _gps_coordinate(
                    gps_data.get("GPSLongitude"), gps_data.get("GPSLongitudeRef")
                )
                if latitude is not None and longitude is not None:
                    gps = {
                        "latitude": latitude,
                        "longitude": longitude,
                        "altitude": gps_data.get("GPSAltitude")
                        and _ratio_to_float(gps_data["GPSAltitude"]),
                    }

    return metadata, {"image_info": image_info, "gps": gps}


def _extract_exifread_metadata(image_path: Path) -> dict[str, str]:
    with image_path.open("rb") as file:
        tags = exifread.process_file(file, details=True, strict=False)

    return {key: _stringify(value) for key, value in tags.items()}


def _file_hashes(payload: bytes) -> dict[str, str]:
    return {
        "md5": hashlib.md5(payload).hexdigest(),
        "sha1": hashlib.sha1(payload).hexdigest(),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def extract_image_metadata(
    *,
    payload: bytes,
    image_path: Path,
    filename: str,
    content_type: str | None,
) -> dict[str, object]:
    if not content_type or not content_type.startswith("image/"):
        raise InvalidInputError("Uploaded file must be an image.")

    diagnostics: dict[str, object] = {
        "has_metadata": False,
        "sources_used": [],
        "warnings": [],
    }

    pillow_metadata: dict[str, str] = {}
    image_info: dict[str, object] = {}
    gps: dict[str, object] = {}

    try:
        pillow_metadata, pillow_extra = _extract_pillow_metadata(image_path)
        image_info = pillow_extra["image_info"]
        gps = pillow_extra["gps"]
        diagnostics["sources_used"].append("pillow")
    except Exception as error:
        diagnostics["warnings"].append(f"Pillow extraction warning: {error}")

    exifread_metadata: dict[str, str] = {}
    try:
        exifread_metadata = _extract_exifread_metadata(image_path)
        diagnostics["sources_used"].append("exifread")
    except Exception as error:
        diagnostics["warnings"].append(f"ExifRead extraction warning: {error}")

    diagnostics["has_metadata"] = bool(pillow_metadata or exifread_metadata or gps)

    return {
        "file_info": {
            "filename": filename,
            "content_type": content_type,
            "size_bytes": len(payload),
            "extension": image_path.suffix.lower().lstrip("."),
            "hashes": _file_hashes(payload),
        },
        "image_info": image_info,
        "gps": gps,
        "metadata": {
            "pillow": pillow_metadata,
            "exifread": exifread_metadata,
        },
        "diagnostics": diagnostics,
    }
