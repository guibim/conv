import xml.etree.ElementTree as ET


def convert_txt_to_xml(input_path: str, output_path: str):
    """
    Converte um arquivo TXT em XML.
    Cada linha do TXT vira um elemento <line>.
    """

    root = ET.Element("document")

    # TXT pode ter encoding variado → leitura tolerante
    with open(input_path, "r", encoding="utf-8", errors="ignore") as file:
        for idx, line in enumerate(file, start=1):
            text = line.strip()
            if not text:
                continue

            line_el = ET.SubElement(root, "line", number=str(idx))
            line_el.text = text

    tree = ET.ElementTree(root)
    tree.write(
        output_path,
        encoding="utf-8",
        xml_declaration=True
    )
