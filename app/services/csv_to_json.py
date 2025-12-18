import json
from itertools import zip_longest

from app.services.utils.csv_reader import read_csv_with_fallback, CSVEncodingError


def convert_csv_to_json(input_path, output_path):
    rows = read_csv_with_fallback(input_path)

    if not rows:
        raise CSVEncodingError("Arquivo CSV vazio ou inválido.")

    header, *body = rows
    data = [
        {key: value for key, value in zip_longest(header, row, fillvalue="")}
        for row in body
    ]

    with open(output_path, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)
