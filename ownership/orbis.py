import os
import pandas as pd

from dotenv import load_dotenv, find_dotenv

from pandas.io.sas.sas7bdat import SAS7BDATReader
from pandas.errors import OutOfBoundsDatetime

load_dotenv(find_dotenv())

def import_data(path):
    return pd.read_sas(path, chunksize=int(20_000))

def look_for(
    comp:str, data_generator:SAS7BDATReader,
    col_names = ["AKANAME", "_890201"],
    verbose = False
) -> pd.DataFrame:

    is_comp_name = lambda ns: any(comp in str(n).lower() for n in ns)

    results = []

    for i, chunk in enumerate(data_generator):
        try:
            verbose and print(f"Chunk: {i + 1}", end="\r")

            company_idx = chunk[col_names].apply(is_comp_name, axis = 1)
            results.append(chunk[company_idx])
        except OutOfBoundsDatetime as error:
            print(f"\n{error}\n")

    return pd.concat(results)