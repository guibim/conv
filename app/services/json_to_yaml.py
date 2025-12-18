def json_to_yaml(json_bytes: bytes) -> bytes:
    data = json.loads(json_bytes)

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
