from app.converters.core import (
    convert_csv_to_html,
    convert_csv_to_json,
    convert_csv_to_txt,
    convert_csv_to_xml,
    convert_html_to_txt,
    convert_json_to_csv,
    convert_json_to_txt,
    convert_json_to_xml,
    convert_txt_to_csv,
    convert_txt_to_json,
    convert_txt_to_xml,
    convert_xml_to_csv,
    convert_xml_to_json,
)
from app.models import ConversionSpec


def _spec(
    source_format: str,
    target_format: str,
    handler,
    media_type: str,
    extension: str,
    stability: str = "stable",
    notes: str = "",
) -> ConversionSpec:
    return ConversionSpec(
        source_format=source_format,
        target_format=target_format,
        handler=handler,
        media_type=media_type,
        extension=extension,
        stability=stability,
        notes=notes,
    )


CONVERSIONS: dict[tuple[str, str], ConversionSpec] = {
    ("txt", "csv"): _spec("txt", "csv", convert_txt_to_csv, "text/csv; charset=utf-8", "csv"),
    ("csv", "txt"): _spec("csv", "txt", convert_csv_to_txt, "text/plain; charset=utf-8", "txt"),
    ("csv", "json"): _spec("csv", "json", convert_csv_to_json, "application/json", "json"),
    ("json", "csv"): _spec("json", "csv", convert_json_to_csv, "text/csv; charset=utf-8", "csv"),
    ("csv", "xml"): _spec("csv", "xml", convert_csv_to_xml, "application/xml", "xml", notes="Column names are sanitized into XML-safe tags."),
    ("xml", "csv"): _spec("xml", "csv", convert_xml_to_csv, "text/csv; charset=utf-8", "csv", notes="Only simple repetitive XML structures are supported."),
    ("csv", "html"): _spec("csv", "html", convert_csv_to_html, "text/html; charset=utf-8", "html"),
    ("html", "txt"): _spec("html", "txt", convert_html_to_txt, "text/plain; charset=utf-8", "txt", notes="Lightweight text extraction, not full DOM rendering."),
    ("txt", "json"): _spec("txt", "json", convert_txt_to_json, "application/json", "json"),
    ("json", "txt"): _spec("json", "txt", convert_json_to_txt, "text/plain; charset=utf-8", "txt"),
    ("txt", "xml"): _spec("txt", "xml", convert_txt_to_xml, "application/xml", "xml"),
    ("json", "xml"): _spec("json", "xml", convert_json_to_xml, "application/xml", "xml", stability="beta"),
    ("xml", "json"): _spec("xml", "json", convert_xml_to_json, "application/json", "json", stability="beta"),
}


def get_conversion(source_format: str, target_format: str) -> ConversionSpec | None:
    return CONVERSIONS.get((source_format.lower(), target_format.lower()))


def list_conversions() -> list[dict[str, str]]:
    items = []
    for spec in sorted(CONVERSIONS.values(), key=lambda item: (item.source_format, item.target_format)):
        items.append(
            {
                "from_format": spec.source_format,
                "to_format": spec.target_format,
                "stability": spec.stability,
                "notes": spec.notes,
            }
        )
    return items
