import pandas as pd
from datetime import datetime
from typing import List
from wave_api.date_settings.wave_date_manager import WaveDateManager


def date_settings(df: pd.DataFrame, dates: List[datetime]) -> List[str]:
    # Analyse random date to identify date format
    # Because Wave is fucking inconsistent "1 Sep 20" or 1 Sep 2020"
    random_date = df.iloc[0, 1]
    wave_date_manager = WaveDateManager()
    wave_date_manager.get_date_type(sample_wave_date=random_date)

    # Convert datetime dates to Wave date format
    arr = []
    for date in dates:
        day = wave_date_manager.get_day(date=date)
        month = wave_date_manager.get_month(date=date)
        year = wave_date_manager.get_year(date=date)
        wave_date = wave_date_manager.get_date_wave_format(
            day=day,
            month=month,
            year=year,
        )
        arr.append(wave_date)
    return arr
