import csv, json

def convert_json_to_csv(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

    if not isinstance(data, list):
        raise ValueError("JSON precisa ser uma lista de objetos (list[dict]).")

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
