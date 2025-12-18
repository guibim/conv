import re
import csv

def convert_ifc_to_csv(input_path: str, output_path: str):
    entity_count = {}

    with open(input_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            match = re.search(r"=IFC([A-Z0-9_]+)\(", line)
            if match:
                entity = f"IFC{match.group(1)}"
                entity_count[entity] = entity_count.get(entity, 0) + 1

    with open(output_path, "w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["Entity", "Count"])
        for entity, count in sorted(entity_count.items()):
            writer.writerow([entity, count])
