import os
import dotenv

import pandas as pd

dotenv.load_dotenv(dotenv.find_dotenv())

password = os.environ.get("PASSWORD", "")
usr = os.environ.get("USR", "")

def import_xls(path:str, datastart=35, dataend=4) -> pd.DataFrame:
    raw_xls = pd.read_excel(path)
    
    data = raw_xls.iloc[datastart:-dataend]
    data.columns = raw_xls.iloc[datastart - 1]

    return data.reset_index(drop=True)
