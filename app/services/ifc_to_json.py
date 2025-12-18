import re
import json

def convert_ifc_to_json(input_path: str, output_path: str):
    entity_count = {}
    schema = None

    with open(input_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            if not schema and "FILE_SCHEMA" in line:
                schema = line.strip()

            match = re.search(r"=IFC([A-Z0-9_]+)\(", line)
            if match:
                entity = f"IFC{match.group(1)}"
                entity_count[entity] = entity_count.get(entity, 0) + 1

    summary = {
        "schema": schema,
        "total_entities": sum(entity_count.values()),
        "entities": dict(sorted(entity_count.items()))
    }

    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(summary, out, indent=2, ensure_ascii=False)
