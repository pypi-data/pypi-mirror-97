import pandas as pd


def search_in_df(
    search_metric: str,
    search_date: str,
    metric_df_dict: dict,
    date_df_dict: dict,
    df: pd.DataFrame,
) -> str:
    index_of_metric = metric_df_dict[search_metric]
    index_of_date = date_df_dict[search_date]
    val = df.iloc[index_of_metric, index_of_date]
    return val
