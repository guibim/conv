import csv
import pyreadstat
import tempfile

def convert_csv_to_dta(input_path, output_path):
    df = []
    
    with open(input_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            df.append(row)

    # pyreadstat aceita lista de dicts
    pyreadstat.write_dta(df, output_path)
