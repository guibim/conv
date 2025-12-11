import csv
import xml.etree.ElementTree as ET

def convert_xml_to_csv(input_path, output_path):
    tree = ET.parse(input_path)
    root = tree.getroot()

    rows = []
    fieldnames = set()

    # Detecta campos
    for item in root.findall("item"):
        row = {}
        for child in item:
            row[child.tag] = child.text
            fieldnames.add(child.tag)
        rows.append(row)

    fieldnames = list(fieldnames)

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
