import pandas_lite as pd
import pyreadstat

def convert_csv_to_dta(input_path: str, output_path: str):
    df = pd.read_csv(input_path)
    pyreadstat.write_dta(df, output_path)
