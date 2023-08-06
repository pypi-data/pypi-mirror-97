import pandas as pd
from typing import List, TypeVar
from wave_api.get_google_sheets_data import get_google_sheets_data
from wave_api.df_converter import DfConverter
from wave_api.search_in_df import search_in_df
from wave_api.wave_data_manager import WaveDateManager

PD_TIMESTAMP = TypeVar('pd.Timestamp')


def create_portfolio(
    google_credentials_filepath: str,
    option: str,
    google_sheets_id: str,
    google_sheets_name: str,
    arr_of_metrics: List[str],
    arr_of_dates: List[PD_TIMESTAMP],
):
    wave_data_manager = WaveDateManager()
    if option == 'Calendar months':
        google_sheets_data = get_google_sheets_data(
            google_sheets_id='1aLar-TcU5cDBaP8FX3k5A1MXYEzT0jDHR9nhtGoSHTI',
            google_sheets_name='Actual Portfolio (26th Feb)',
            google_credentials_filepath=google_credentials_filepath,
        )
        df = pd.DataFrame(data=google_sheets_data)

        # Select a random date because Wave is fucking inconsistent "1 Sep 20" or 1 Sep 2020"
        # Info is saved in class instance
        random_date = df.iloc[0, 1]
        wave_data_manager.get_date_type(sample_wave_date=random_date)

        # Get mappings (dictionary) of Dataframe's rows and cols
        df_converter = DfConverter(df)
        metric_df_dict = df_converter.get_metric_dict()
        date_df_dict = df_converter.get_date_dict()

        # Convert pd.Timestamp to Wave date format
        arr = []
        for date in arr_of_dates:
            day = wave_data_manager.get_day(date=date)
            month = wave_data_manager.get_month(date=date)
            year = wave_data_manager.get_year(date=date)
            wave_date = wave_data_manager.get_date_wave_format(
                day=day,
                month=month,
                year=year,
            )
            arr.append(wave_date)

        # Get data and store as dictionary of dictionaries
        big_dict = {}
        for metric in arr_of_metrics:
            sub_dict = {}
            for date in arr:
                val = search_in_df(
                    search_metric=metric,
                    search_date=date,
                    metric_df_dict=metric_df_dict,
                    date_df_dict=date_df_dict,
                    df=df,
                )
                sub_dict[date] = val

            big_dict[metric] = sub_dict  # Append dictionary to dictionary

        return big_dict