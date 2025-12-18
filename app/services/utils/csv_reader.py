import csv
import io

class CSVEncodingError(Exception):
    pass


def read_csv_with_fallback(file_path: str):
    """
    Lê CSV tentando múltiplos encodings.
    Retorna lista de linhas (list[list[str]]).
    """

    encodings_to_try = [
        "utf-8",
        "utf-8-sig",
        "windows-1252",
        "latin-1",
    ]

    last_error = None

    for encoding in encodings_to_try:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                reader = csv.reader(f)
                rows = list(reader)
                return rows
        except UnicodeDecodeError as e:
            last_error = e
            continue

    raise CSVEncodingError(
        "Não foi possível decodificar o arquivo CSV. "
        "Encodings testados: utf-8, utf-8-sig, windows-1252, latin-1."
    )
