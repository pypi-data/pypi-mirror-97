"""Filter event frames in Pandas DataFrames tables or merge DataFrame-backed event frame lists."""

from datetime import datetime

import pandas as pd


def filter_series(series: pd.DataFrame, event_frames: pd.DataFrame) -> pd.DataFrame:
    """Filter the even_frames out of the series."""
    if len(series) == 0:
        return series

    for index, start_date in enumerate(event_frames['start_date']):
        end_date = event_frames['end_date'][index]
        # pylint: disable=no-member
        series = series.loc[(series['ts'] < start_date) | (series['ts'] > end_date)]
    return series


def filter_event_frames(event_frames: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Restrict time range to filter event frames."""
    if len(event_frames) == 0:
        return event_frames

    filtered = event_frames.loc[
        (event_frames['start_date'] > pd.to_datetime(end_date)) |
        (event_frames['end_date'] > pd.to_datetime(start_date))
        ].copy()

    filtered.loc[filtered['start_date'] < pd.to_datetime(start_date), 'start_date'] = pd.to_datetime(start_date)
    filtered.loc[filtered['end_date'] > pd.to_datetime(end_date), 'end_date'] = pd.to_datetime(end_date)
    return filtered
