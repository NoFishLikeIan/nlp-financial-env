def pct_to_num(pct) -> float:
    """
    Convert 1% to 0.01
    """
    if type(pct) == str:
        return float(pct.replace("%", "")) / 100

    return pct

def parse_ownership_data(raw):
    df = raw.dropna(axis = 0, how = 'all').dropna(axis = 1, how = 'all').dropna(axis = 0, how = 'any')

    investors = df.columns[-7:]
    for investor in investors:
        df[investor] = df[investor].apply(pct_to_num)

    return df