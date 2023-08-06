import pandas as pd
import io
from slugify import slugify


def to_df(csv: str) -> pd.DataFrame:
    return pd.read_csv(io.StringIO(csv), header=1, delimiter=";")[:-1]


def clean(data: pd.DataFrame) -> pd.DataFrame:
    """Set relevant type and normalize header name"""
    df = data.copy()
    df["Code libellé"] = df["Code libellé"].astype(int)
    for num in ["Mini", "Maxi", "Moyen"]:
        df[num] = df[num].str.replace(",", ".").astype(float)
    df.columns = [slugify(col, separator="_") for col in df.columns]
    return df


def process_csv(raw: str) -> pd.DataFrame:
    "transform raw csv text to a dataframe with clean header"
    return clean(to_df(raw))


def get_recent(df: pd.DataFrame, sortby, keys: list) -> pd.DataFrame:
    """Only keep the most recente occurence for each row
    `keys` is the subset of cols to consider
    """
    return df.sort_values(sortby).drop_duplicates(subset=keys, keep="last")