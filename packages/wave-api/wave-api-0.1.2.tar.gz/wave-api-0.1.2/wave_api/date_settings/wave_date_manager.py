import calendar  # Get month name from month no
import pandas as pd
from typing import TypeVar

PD_TIMESTAMP = TypeVar('pd.Timestamp')


class WaveDateManager():
    '''
    Convert pd.Timestamp to Wave date format

    Step 1: Get the day, month and year individually 
    Step 2: Some of these class variables can be None
    Step 3: Join them together to get the final Wave date
    '''
    def __init__(
        self,
        with_day=None,
        with_month=None,
        with_year=None,
        type_of_year=None,
    ) -> None:
        self.with_day = with_day
        self.with_month = with_month
        self.with_year = with_year
        self.type_of_year = type_of_year
        pass

    def get_date_type(self, sample_wave_date: str) -> None:
        arr = sample_wave_date.split(' ')
        year = arr[-1]

        # Wave is fucking inconsistent with its dates ('21' vs '2021')
        if len(year) == 2:
            self.type_of_year = '2-digit year'
        elif len(year) == 4:
            self.type_of_year = '4-digit year'

    def get_day(self, date: PD_TIMESTAMP) -> str:
        return date.day

    def get_month(self, date: PD_TIMESTAMP) -> str:
        month = date.month
        # Convert month no to month name
        month = calendar.month_name[month]
        month = month[0:3]
        return month

    def get_year(self, date: PD_TIMESTAMP) -> str:
        year = str(date.year)
        # e.g. '21' vs '2021'
        if self.type_of_year == '2-digit year':
            return year[-2:]
        elif self.type_of_year == '4-digit year':
            return year

    def get_date_wave_format(self, day: str, month: str, year: str) -> str:
        return f'{day} {month} {year}'
