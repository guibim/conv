import json


def _read_txt_lines(input_path: str):
    encodings = ["utf-8", "utf-8-sig", "windows-1252", "latin-1"]
    last_error = None

    for encoding in encodings:
        try:
            with open(input_path, "r", encoding=encoding) as txtfile:
                return txtfile.readlines()
        except UnicodeDecodeError as error:
            last_error = error
            continue

    raise UnicodeDecodeError("", b"", 0, 1, "Falha ao decodificar TXT") from last_error


def convert_txt_to_json(input_path, output_path):
    lines = [line.strip() for line in _read_txt_lines(input_path) if line.strip()]

    with open(output_path, "w", encoding="utf-8") as jsonfile:
        json.dump(lines, jsonfile, indent=2, ensure_ascii=False)
