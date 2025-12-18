import json


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


def json_to_yaml(json_bytes: bytes) -> bytes:
    data = _decode_json_bytes(json_bytes)

    def dump(obj, indent=0):
        space = "  " * indent
        if isinstance(obj, dict):
            lines = []
            for k, v in obj.items():
                lines.append(f"{space}{k}:")
                lines.append(dump(v, indent + 1))
            return "\n".join(lines)
        elif isinstance(obj, list):
            return "\n".join(f"{space}- {dump(v, indent + 1).lstrip()}" for v in obj)
        else:
            return f"{space}{obj}"

    return dump(data).encode("utf-8")
