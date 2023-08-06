from typing import List, TypeVar
from datetime import datetime


class Options:
    def __init__(
        self,
        timeline: str,
        metrics: List[str],
        wave_dates: List[datetime],
    ):
        '''
        Timeline -> Monthly, Yearly, or Quaterly
        Metrics -> "Seedin Investment", "UOB One (Tuition)"
        Dates -> datetime(2020, 1, 31)
        '''
        self.timeline = timeline
        self.metrics = metrics
        self.wave_dates = wave_dates
