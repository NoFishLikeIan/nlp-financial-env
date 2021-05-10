import os
import pandas as pd

from typing import List

from dotenv import load_dotenv, find_dotenv

from pandas.io.sas.sas7bdat import SAS7BDATReader
from pandas.errors import OutOfBoundsDatetime

load_dotenv(find_dotenv())

def import_data(path):
    return pd.read_sas(path, chunksize=int(20_000))

def look_for(
    comp:str, data_generator:SAS7BDATReader,
    col_names = ["AKANAME", "_890201"],
    verbose = False) -> List[bytes]:

    is_comp_name = lambda ns: any(comp in str(n).lower() for n in ns)

    found_dfs = []

    i = 0

    # TODO: Find better way to handle iterator
    while True:
        i += 1
        try:
            chunk = next(data_generator)
            company_idx = chunk[col_names].apply(
                is_comp_name, 
                axis = 1
            )

            found_dfs.append(chunk[company_idx])

            verbose and print(f"Chunk {i}", end = "\r")

        except (ValueError, OutOfBoundsDatetime) as error: 
            # Error with reading data
            print(f"\n{error}\n")


        except StopIteration: 
            # End of iteration
            break

    bvdid = pd.concat(found_dfs)["bvdid"].tolist()


    return bvdid

