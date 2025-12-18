import json
import xml.etree.ElementTree as ET


def _decode_json_bytes(json_bytes: bytes):
    encodings = ["utf-8", "utf-8-sig", "windows-1252", "latin-1"]
    last_error = None

    for encoding in encodings:
        try:
            return json.loads(json_bytes.decode(encoding))
        except UnicodeDecodeError as error:
            last_error = error
            continue

    raise UnicodeDecodeError("", b"", 0, 1, "Falha ao decodificar JSON") from last_error


def json_to_xml(json_bytes: bytes) -> bytes:
    data = _decode_json_bytes(json_bytes)

    def build(parent, value):
        if isinstance(value, dict):
            for k, v in value.items():
                child = ET.SubElement(parent, k)
                build(child, v)
        elif isinstance(value, list):
            for item in value:
                item_el = ET.SubElement(parent, "item")
                build(item_el, item)
        else:
            parent.text = str(value)

    root = ET.Element("root")
    build(root, data)
    return ET.tostring(root, encoding="utf-8")
