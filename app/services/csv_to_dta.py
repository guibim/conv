import pandas as pd
import pyreadstat

def convert_csv_to_dta(input_path: str, output_path: str):
    """
    Converte um arquivo .csv para .dta (Stata)
    """
    df = pd.read_csv(input_path)
    pyreadstat.write_dta(df, output_path)
