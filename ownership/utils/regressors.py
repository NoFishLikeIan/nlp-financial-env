import pandas as pd

def parse_regressors(raw:pd.DataFrame):

    firms = raw.iloc[2:, 1].rename("Firms")

    index_chunk = [
        *(i for i, x in enumerate(raw.loc[0]) if not pd.isna(x)),
        -1
    ]

    index_pairs = list(zip(index_chunk, index_chunk[1:]))

    dfs = []

    for i, j in index_pairs:

        chunk_raw = raw.reset_index(drop = True)
        chunk_df = chunk_raw.iloc[2:, i:(j - 1)]

        year = raw.iloc[0, i].split('/')[-1]
        chunk_df.columns = [f"{col}-{year}" for col in chunk_raw.iloc[1, i:(j - 1)]]

        chunk_df = chunk_df.set_index(firms)
        dfs.append(chunk_df)

    df = pd.concat(dfs, axis = 1).apply(pd.to_numeric, axis = 0)

    return df

    
if __name__ == "__main__":
    
    from dotenv import load_dotenv
    import os

    load_dotenv()

    data_path = os.path.join("..", os.environ.get("DATA_PATH"))
    reg_path = os.path.join(data_path, "controls.csv")

    raw = pd.read_csv(reg_path)
    df = parse_regressors(raw)


    
