import pandas as pd
from typing import List
from wave_api.create_portfolio.df_converter import DfConverter
from wave_api.options import Options


def create_portfolio(df: pd.DataFrame, options: Options):
    option = options.timeline
    metrics = options.metrics
    wave_dates = options.wave_dates

    if option == 'Monthly':
        # Get mappings (dictionary) of Dataframe's rows and cols
        df_converter = DfConverter(df)
        metric_df_dict = df_converter.get_metric_dict()
        date_df_dict = df_converter.get_date_dict()

        # Get data and store as dictionary of dictionaries
        data = {}
        for metric in metrics:
            sub_data = {}
            for date in wave_dates:
                val = df_converter.search_in_df(
                    search_metric=metric,
                    search_date=date,
                    metric_df_dict=metric_df_dict,
                    date_df_dict=date_df_dict,
                )
                sub_data[date] = val
            data[metric] = sub_data  # Append dictionary to dictionary
        return data
