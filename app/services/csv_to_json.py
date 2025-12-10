import csv, json

def convert_csv_to_json(input_path, output_path):
    with open(input_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    with open(output_path, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=2)
