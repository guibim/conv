import re

def convert_ifc_to_txt(input_path: str, output_path: str):
    entities = []

    with open(input_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            match = re.search(r"=IFC([A-Z0-9_]+)\(", line)
            if match:
                entities.append(f"IFC{match.group(1)}")

    with open(output_path, "w", encoding="utf-8") as out:
        for entity in entities:
            out.write(entity + "\n")
