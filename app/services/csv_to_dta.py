from itertools import zip_longest

import pandas_lite as pd
import pyreadstat

from app.services.utils.csv_reader import read_csv_with_fallback, CSVEncodingError


def convert_csv_to_dta(input_path: str, output_path: str):
    rows = read_csv_with_fallback(input_path)

    if not rows:
        raise CSVEncodingError("Arquivo CSV vazio ou inválido.")

    header, *body = rows
    normalized_body = [
        list(zip_longest(header, row, fillvalue="")) for row in body
    ]

    data = {col: [] for col in header}
    for row in normalized_body:
        for column, value in row:
            data[column].append(value)

    df = pd.DataFrame(data)
    pyreadstat.write_dta(df, output_path)
