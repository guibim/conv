import json
from itertools import zip_longest
from xml.etree import ElementTree as ET

from app.errors import InvalidInputError, InvalidStructureError
from app.models import ConversionContext, ConversionResult

from app.converters.common import (
    csv_rows_to_html_document,
    decode_text_with_fallback,
    extract_text_lines,
    html_to_text,
    parse_csv_rows,
    parse_json_payload,
    rows_to_csv_bytes,
    safe_xml_name,
    xml_root_to_rows,
)


def convert_txt_to_csv(payload: bytes, context: ConversionContext) -> ConversionResult:
    rows = [[line] for line in extract_text_lines(payload)]
    return ConversionResult(
        output_bytes=rows_to_csv_bytes(rows),
        media_type="text/csv; charset=utf-8",
        extension="csv",
    )


def convert_csv_to_txt(payload: bytes, context: ConversionContext) -> ConversionResult:
    rows = parse_csv_rows(payload)
    text = "\n".join(" | ".join(row) for row in rows)
    return ConversionResult(
        output_bytes=text.encode("utf-8"),
        media_type="text/plain; charset=utf-8",
        extension="txt",
    )


def convert_csv_to_json(payload: bytes, context: ConversionContext) -> ConversionResult:
    rows = parse_csv_rows(payload)
    if not rows:
        raise InvalidInputError("CSV payload is empty.")

    header, *body = rows
    if not header:
        raise InvalidStructureError("CSV header row is empty.")

    data = [
        {key: value for key, value in zip_longest(header, row, fillvalue="")}
        for row in body
    ]

    return ConversionResult(
        output_bytes=json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"),
        media_type="application/json",
        extension="json",
    )


def convert_json_to_csv(payload: bytes, context: ConversionContext) -> ConversionResult:
    data = parse_json_payload(payload)
    if not isinstance(data, list):
        raise InvalidStructureError("JSON payload must be a list of objects.")

    if not data:
        return ConversionResult(
            output_bytes=b"",
            media_type="text/csv; charset=utf-8",
            extension="csv",
        )

    if not all(isinstance(item, dict) for item in data):
        raise InvalidStructureError("JSON payload must contain only objects.")

    fieldnames: list[str] = []
    for item in data:
        for key in item.keys():
            if key not in fieldnames:
                fieldnames.append(str(key))

    rows = [fieldnames]
    for item in data:
        rows.append([str(item.get(field, "")) for field in fieldnames])

    return ConversionResult(
        output_bytes=rows_to_csv_bytes(rows),
        media_type="text/csv; charset=utf-8",
        extension="csv",
    )


def convert_csv_to_xml(payload: bytes, context: ConversionContext) -> ConversionResult:
    rows = parse_csv_rows(payload)
    if not rows:
        raise InvalidInputError("CSV payload is empty.")

    headers, *body = rows
    if not headers:
        raise InvalidStructureError("CSV header row is empty.")

    root = ET.Element("root")
    xml_headers = [safe_xml_name(header, index) for index, header in enumerate(headers)]

    for row in body:
        item = ET.SubElement(root, "item")
        for key, value in zip_longest(xml_headers, row, fillvalue=""):
            child = ET.SubElement(item, key)
            child.text = value or ""

    return ConversionResult(
        output_bytes=ET.tostring(root, encoding="utf-8", xml_declaration=True),
        media_type="application/xml",
        extension="xml",
    )


def convert_xml_to_csv(payload: bytes, context: ConversionContext) -> ConversionResult:
    rows = xml_root_to_rows(payload)
    return ConversionResult(
        output_bytes=rows_to_csv_bytes(rows),
        media_type="text/csv; charset=utf-8",
        extension="csv",
    )


def convert_csv_to_html(payload: bytes, context: ConversionContext) -> ConversionResult:
    rows = parse_csv_rows(payload)
    html = csv_rows_to_html_document(rows)
    return ConversionResult(
        output_bytes=html.encode("utf-8"),
        media_type="text/html; charset=utf-8",
        extension="html",
    )


def convert_html_to_txt(payload: bytes, context: ConversionContext) -> ConversionResult:
    text = html_to_text(payload)
    return ConversionResult(
        output_bytes=text.encode("utf-8"),
        media_type="text/plain; charset=utf-8",
        extension="txt",
    )


def convert_txt_to_json(payload: bytes, context: ConversionContext) -> ConversionResult:
    lines = [line for line in extract_text_lines(payload) if line]
    return ConversionResult(
        output_bytes=json.dumps(lines, indent=2, ensure_ascii=False).encode("utf-8"),
        media_type="application/json",
        extension="json",
    )


def convert_json_to_txt(payload: bytes, context: ConversionContext) -> ConversionResult:
    data = parse_json_payload(payload)
    if not isinstance(data, list):
        raise InvalidStructureError("JSON payload must be a list of values.")

    text = "\n".join(str(item) for item in data)
    return ConversionResult(
        output_bytes=text.encode("utf-8"),
        media_type="text/plain; charset=utf-8",
        extension="txt",
    )


def convert_txt_to_xml(payload: bytes, context: ConversionContext) -> ConversionResult:
    root = ET.Element("document")
    for line_number, line in enumerate(extract_text_lines(payload), start=1):
        if not line:
            continue
        element = ET.SubElement(root, "line", number=str(line_number))
        element.text = line

    return ConversionResult(
        output_bytes=ET.tostring(root, encoding="utf-8", xml_declaration=True),
        media_type="application/xml",
        extension="xml",
    )


def convert_json_to_xml(payload: bytes, context: ConversionContext) -> ConversionResult:
    data = parse_json_payload(payload)

    def build(parent: ET.Element, value) -> None:
        if isinstance(value, dict):
            for key, child_value in value.items():
                child = ET.SubElement(parent, safe_xml_name(str(key), 0))
                build(child, child_value)
        elif isinstance(value, list):
            for item in value:
                child = ET.SubElement(parent, "item")
                build(child, item)
        else:
            parent.text = "" if value is None else str(value)

    root = ET.Element("root")
    build(root, data)

    return ConversionResult(
        output_bytes=ET.tostring(root, encoding="utf-8", xml_declaration=True),
        media_type="application/xml",
        extension="xml",
    )


def convert_xml_to_json(payload: bytes, context: ConversionContext) -> ConversionResult:
    from app.converters.common import parse_xml_root

    root = parse_xml_root(payload)

    def parse(element: ET.Element):
        children = list(element)
        if not children:
            return element.text or ""

        result: dict[str, list] = {}
        for child in children:
            result.setdefault(child.tag, []).append(parse(child))

        normalized = {}
        for key, values in result.items():
            normalized[key] = values[0] if len(values) == 1 else values
        return normalized

    return ConversionResult(
        output_bytes=json.dumps(parse(root), indent=2, ensure_ascii=False).encode(
            "utf-8"
        ),
        media_type="application/json",
        extension="json",
    )
