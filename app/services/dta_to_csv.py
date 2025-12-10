import pyreadstat
import pandas as pd

def convert_dta_to_csv(input_path: str, output_path: str):
    """
    Converte um arquivo .dta (Stata) para .csv
    """
    df, meta = pyreadstat.read_dta(input_path)
    df.to_csv(output_path, index=False)
