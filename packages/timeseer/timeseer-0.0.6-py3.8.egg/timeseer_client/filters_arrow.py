"""Filter event frames in Arrow tables or merge Arrow-backed event frame lists."""

from typing import List
from datetime import datetime

import pyarrow as pa
import pyarrow.compute as pc


def filter_series(series: pa.Table, event_frames: pa.Table) -> pa.Table:
    """Filter the even_frames out of the series."""
    if series.num_rows == 0:
        return series

    total: List[bool] = [True] * series.num_rows
    for index, start_date in enumerate(event_frames['start_date']):
        # pylint: disable=no-member
        on_or_after = pc.less(series['ts'], start_date)
        before = pc.greater(series['ts'], event_frames['end_date'][index])
        out_event_frame = pc.or_(on_or_after, before)
        total = pc.and_(total, out_event_frame)
    return series.filter(total)


def filter_event_frames(event_frames: pa.Table, start_date: datetime, end_date: datetime) -> pa.Table:
    """Restrict time range to filter event frames."""
    if event_frames.num_rows == 0:
        return event_frames

    new_start_dates = []
    new_end_dates = []
    total: List[bool] = [True] * event_frames.num_rows
    for index, start_date_frame in enumerate(event_frames['start_date']):
        end_date_frame = event_frames['end_date'][index]
        # pylint: disable=no-member
        out_start = pc.greater_equal(start_date_frame, pa.scalar(end_date))
        out_end = pc.less_equal(end_date_frame, pa.scalar(start_date))
        new_start_date = start_date_frame.as_py()
        new_end_date = end_date_frame.as_py()
        if out_start.as_py() or out_end.as_py():
            total[index] = False
        if pc.less(start_date_frame, pa.scalar(start_date)).as_py():
            new_start_date = start_date
        if pc.greater(end_date_frame, pa.scalar(end_date)).as_py():
            new_end_date = end_date
        new_start_dates.append(new_start_date)
        new_end_dates.append(new_end_date)
    new_table = event_frames.set_column(
                    0,
                    'start_date',
                    pa.array(new_start_dates, type=pa.timestamp('us', tz='UTC'))
                )
    new_table = new_table.set_column(
                    1,
                    'end_date',
                    pa.array(new_end_dates, type=pa.timestamp('us', tz='UTC'))
                )
    return new_table.filter(total)
