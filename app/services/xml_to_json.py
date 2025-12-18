def xml_to_json(xml_bytes: bytes) -> bytes:
    def parse(elem):
        if len(elem) == 0:
            return elem.text
        result = {}
        for child in elem:
            result.setdefault(child.tag, []).append(parse(child))
        return {k: v[0] if len(v) == 1 else v for k, v in result.items()}

    root = ET.fromstring(xml_bytes)
    return json.dumps(parse(root), indent=2).encode("utf-8")
