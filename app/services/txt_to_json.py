import json

def convert_txt_to_json(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as txtfile:
        lines = [line.strip() for line in txtfile.readlines() if line.strip()]

    with open(output_path, "w", encoding="utf-8") as jsonfile:
        json.dump(lines, jsonfile, indent=2, ensure_ascii=False)
