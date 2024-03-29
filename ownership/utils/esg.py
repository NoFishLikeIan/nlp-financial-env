from typing import Callable

import pandas as pd
import numpy as np

"""
From raw .xlsx ESG data construct a function of year that yields pd.DataFrame with companies as row, type of index as columns, and scores.
"""
def yearly_esg_maker(raw:pd.DataFrame) -> Callable[[str, str], pd.DataFrame]:

    data = raw.iloc[3:, :]
    data.columns = raw.iloc[2, :].apply(
        lambda e: str(int(e) if type(e) is np.float64 else str(e)))

    data = data.reset_index(drop = True)

    name_df = data["Name"].str.rsplit("-", n = 1, expand = True)
    data["Name"] = name_df[0]
    data["Data type"] = name_df[1]
        
    def getyear(year):
        if int(year) < 2016 or int(year) > 2021:
            raise ValueError(f"Year {year} not valid. Data only available for period 2016-2021.") 
        
        year_df = pd.pivot_table(data, index = ["Name"], columns=["Data type"], values = [str(year)])[str(year)]

        year_df.index = [s.replace(" ", "") for s in year_df.index]
        year_df.columns = [s.strip() for s in year_df.columns]

        return year_df

    return getyear

if __name__ == "__main__":
    import dotenv, os

    dotenv.load_dotenv()

    data_path = os.path.join("..", os.environ.get("DATA_PATH"))

    esg_path = os.path.join(data_path, "ESG.xlsx")
    sheet_name = os.environ.get("SHEET_NAME")

    raw = pd.read_excel(esg_path, sheet_name = sheet_name)
    get = yearly_esg_maker(raw)

    get(2016)