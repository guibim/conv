import json

def convert_json_to_txt(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

    if not isinstance(data, list):
        raise ValueError("O JSON precisa ser uma lista de valores para conversão para TXT.")

    with open(output_path, "w", encoding="utf-8") as txtfile:
        for item in data:
            txtfile.write(str(item) + "\n")
