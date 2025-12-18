def json_to_xml(json_bytes: bytes) -> bytes:
    data = json.loads(json_bytes)

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
