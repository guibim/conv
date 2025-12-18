import pyreadstat
import csv

def convert_dta_to_csv(input_path, output_path):
    df, meta = pyreadstat.read_dta(input_path)
    df.to_csv(output_path, index=False, encoding="utf-8")
