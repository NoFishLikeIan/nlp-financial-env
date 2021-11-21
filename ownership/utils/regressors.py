import pandas as pd

def parse_regressors(raw:pd.DataFrame):

    firms = raw.iloc[2:, 1].rename("Firms")

    index_chunk = [
        i for i, x in enumerate(raw.loc[0]) 
        if not pd.isna(x)
    ]

    index_pairs = zip(index_chunk, index_chunk[1:])

    dfs = []

    for i, j in index_pairs:
        chunk_raw = raw.reset_index(drop = True)
        chunk_df = chunk_raw.iloc[2:, i:(j - 1)]

        year = raw.iloc[0, i].split('/')[-1]
        chunk_df.columns = [f"{col}-{year}" for col in chunk_raw.iloc[1, i:(j - 1)]]

        chunk_df = chunk_df.set_index(firms)


        dfs.append(chunk_df)

    return pd.concat(dfs, axis = 1)

    

    
