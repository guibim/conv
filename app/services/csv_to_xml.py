import csv
import xml.etree.ElementTree as ET

def convert_csv_to_xml(input_path, output_path):
    # Tenta abrir como UTF-8
    try:
        with open(input_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
    except UnicodeDecodeError:
        # Fallback para arquivos CSV vindos do Excel/Windows
        with open(input_path, newline='', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

    root = ET.Element("root")

    for row in rows:
        item = ET.SubElement(root, "item")
        for key, value in row.items():
            child = ET.SubElement(item, key)
            child.text = value if value is not None else ""

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
