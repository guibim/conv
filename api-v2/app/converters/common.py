import csv
from html import escape as html_escape
from html.parser import HTMLParser
import io
import json
import re

from defusedxml import ElementTree as SafeET

from app.errors import EncodingDetectionError, InvalidInputError, InvalidStructureError


TEXT_ENCODINGS = ("utf-8", "utf-8-sig", "windows-1252", "latin-1")
XML_NAME_PATTERN = re.compile(r"[^a-zA-Z0-9_.-]+")


def decode_text_with_fallback(payload: bytes, label: str) -> str:
    last_error = None
    for encoding in TEXT_ENCODINGS:
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError as error:
            last_error = error

    raise EncodingDetectionError(
        f"Unable to decode {label}. Tried: {', '.join(TEXT_ENCODINGS)}."
    ) from last_error


def parse_csv_rows(payload: bytes) -> list[list[str]]:
    text = decode_text_with_fallback(payload, "CSV payload")
    return list(csv.reader(io.StringIO(text)))


def rows_to_csv_bytes(rows: list[list[str]]) -> bytes:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def parse_json_payload(payload: bytes):
    text = decode_text_with_fallback(payload, "JSON payload")
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        raise InvalidInputError("Invalid JSON payload.") from error


def extract_text_lines(payload: bytes) -> list[str]:
    text = decode_text_with_fallback(payload, "text payload")
    return [line.rstrip("\r\n") for line in text.splitlines()]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        cleaned = data.strip()
        if cleaned:
            self.parts.append(cleaned)


def html_to_text(payload: bytes) -> str:
    parser = TextExtractor()
    parser.feed(decode_text_with_fallback(payload, "HTML payload"))
    return "\n".join(parser.parts)


def safe_xml_name(name: str, index: int) -> str:
    candidate = XML_NAME_PATTERN.sub("_", name.strip())
    if not candidate:
        candidate = f"column_{index + 1}"
    if candidate[0].isdigit():
        candidate = f"column_{index + 1}_{candidate}"
    return candidate


def parse_xml_root(payload: bytes):
    try:
        return SafeET.fromstring(payload)
    except SafeET.ParseError as error:
        raise InvalidInputError("Invalid XML payload.") from error


def xml_root_to_rows(payload: bytes) -> list[list[str]]:
    root = parse_xml_root(payload)
    items = list(root.findall("item"))

    if not items:
        direct_children = list(root)
        if direct_children and all(list(child) for child in direct_children):
            items = direct_children

    if not items:
        raise InvalidStructureError(
            "XML structure is not supported for CSV conversion."
        )

    fieldnames: list[str] = []
    rows: list[list[str]] = []

    for item in items:
        row_map: dict[str, str] = {}
        for child in list(item):
            if child.tag not in fieldnames:
                fieldnames.append(child.tag)
            row_map[child.tag] = child.text or ""
        rows.append([row_map.get(field, "") for field in fieldnames])

    if not fieldnames:
        raise InvalidStructureError(
            "XML structure does not contain tabular child elements."
        )

    return [fieldnames, *rows]


def csv_rows_to_html_document(rows: list[list[str]]) -> str:
    lines = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        "  <title>Converted CSV</title>",
        "  <style>",
        "    body { font-family: Arial, sans-serif; margin: 24px; }",
        "    table { border-collapse: collapse; width: 100%; }",
        "    td, th { border: 1px solid #d0d7de; padding: 8px; text-align: left; }",
        "    tr:nth-child(even) { background: #f6f8fa; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <table>",
    ]

    for row_index, row in enumerate(rows):
        cell_tag = "th" if row_index == 0 else "td"
        escaped_cells = "".join(
            f"    <{cell_tag}>{html_escape(cell)}</{cell_tag}>"
            for cell in row
        )
        lines.append(f"    <tr>{escaped_cells}</tr>")

    lines.extend(["  </table>", "</body>", "</html>"])
    return "\n".join(lines)
