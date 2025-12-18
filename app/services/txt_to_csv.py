import csv


def _read_txt_lines(input_path: str):
    encodings = ["utf-8", "utf-8-sig", "windows-1252", "latin-1"]
    last_error = None

    for encoding in encodings:
        try:
            with open(input_path, "r", encoding=encoding) as txt_file:
                return txt_file.readlines()
        except UnicodeDecodeError as error:
            last_error = error
            continue

    raise UnicodeDecodeError("", b"", 0, 1, "Falha ao decodificar TXT") from last_error


def convert_txt_to_csv(input_path, output_path):
    lines = _read_txt_lines(input_path)

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for line in lines:
            writer.writerow([line.strip()])
