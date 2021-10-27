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
        
        year_df = pd.pivot_table(data, 
            index = ["Name"], columns=["Data type"], values = [str(year)])

        return year_df

    return getyear