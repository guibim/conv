import csv
import xml.etree.ElementTree as ET

def convert_csv_to_xml(input_path, output_path):
    with open(input_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        root = ET.Element("root")

        for row in reader:
            item = ET.SubElement(root, "item")
            for key, value in row.items():
                child = ET.SubElement(item, key)
                child.text = value

        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
