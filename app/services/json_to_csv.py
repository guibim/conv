import csv
import json
from typing import Any


def _load_json_with_fallback(input_path: str) -> Any:
    encodings = ["utf-8", "utf-8-sig", "windows-1252", "latin-1"]
    last_error = None

    for encoding in encodings:
        try:
            with open(input_path, "r", encoding=encoding) as jsonfile:
                return json.load(jsonfile)
        except UnicodeDecodeError as error:
            last_error = error
            continue

    raise UnicodeDecodeError("", b"", 0, 1, "Falha ao decodificar JSON") from last_error


def convert_json_to_csv(input_path, output_path):
    data = _load_json_with_fallback(input_path)

    if not isinstance(data, list):
        raise ValueError("JSON precisa ser uma lista de objetos (list[dict]).")

    if not data:
        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            csvfile.write("")
        return

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
