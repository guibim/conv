import xml.etree.ElementTree as ET
from itertools import zip_longest

from app.services.utils.csv_reader import read_csv_with_fallback, CSVEncodingError


def convert_csv_to_xml(input_path, output_path):
    rows = read_csv_with_fallback(input_path)

    if not rows:
        raise CSVEncodingError("Arquivo CSV vazio ou inválido.")

    header, *body = rows

    root = ET.Element("root")

    for row in body:
        item = ET.SubElement(root, "item")
        for key, value in zip_longest(header, row, fillvalue=""):
            child = ET.SubElement(item, key)
            child.text = value if value is not None else ""

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
