"""Timeseer Client allows querying of data and metadata."""

import json

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Generator, Tuple, Union

import pyarrow as pa
import pyarrow.flight as fl
try:
    import pandas as pd
    import timeseer_client.filters_pandas as filters_pandas
    HAS_PANDAS = True
except Exception:  # pylint: disable=broad-except
    HAS_PANDAS = False

import timeseer_client.filters_arrow as filters_arrow

from timeseer_client import Dictionary, Metadata, SeriesSelector


class Client():
    """Client connects to Timeseer using Arrow Flight."""

    _client: fl.FlightClient = None

    def __init__(self, api_key: Tuple[str, str] = ('', ''), host: str = 'localhost', port: int = 8081):
        """Create a new Client.

        Creating a client does not open a connection. The connection will be opened lazily.

        Args:
            host: the hostname where the Timeseer instance is running. Defaults to ``localhost``.
            port: the port where the Timeseer instance is running. Defaults to ``8081``.
            api_key: the api key for the Timeseer.
        """
        self._location = (host, port)
        self._api_key = api_key

    def search(self, selector: SeriesSelector) -> Generator[Union[Metadata, SeriesSelector], None, None]:
        """Search Timeseer for time series matching the given ``SeriesSelector``.

        Args:
            selector: return time series matching the given selector.
                      Use ``name = None`` (the default) to select all series in a source.

        Returns:
            A generator that returns either ``Metadata`` or ``SeriesSelector``s.
            The return value depends on the search that is supported by the source.
        """
        body = dict(source=selector.source, name=selector.name)
        results = list(self._get_client().do_action(('search', json.dumps(body).encode())))
        for result in results:
            data = json.loads(result.body.to_pybytes())
            if 'series' not in data:
                yield SeriesSelector(data['source'], data['name'])
            else:
                yield _read_metadata(data)

    def get_metadata(self, selector: SeriesSelector) -> Metadata:
        """Read metadata for the time series selected by the ``SeriesSelector``.

        Args:
            selector: the selected time series

        Returns:
            The ``Metadata`` for the time series.
        """
        body = dict(source=selector.source, name=selector.name)
        results = list(self._get_client().do_action(('get_metadata', json.dumps(body).encode())))
        result = results[0]
        data = json.loads(result.body.to_pybytes())
        return _read_metadata(data)

    def get_data(
        self,
        selector: SeriesSelector,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> pa.Table:
        """Get raw data for the time series selected by the SeriesSelector.

        Args:
            selector: return data for the time series selected by this selector.
            start_date: the start date of the time range of data to return. Defaults to one year ago.
            end_date: the end date of the time range of data to return. Defaults to now.

        Returns:
            A pyarrow Table with two columns: 'ts' and 'value'.
        """
        if start_date is None or end_date is None:
            now = datetime.utcnow().replace(tzinfo=timezone(timedelta(0)))
            if start_date is None:
                start_date = now.replace(year=now.year-1)
            if end_date is None:
                end_date = now
        query = {
            'query': 'get_data',
            'selector': {
                'source': selector.source,
                'name': selector.name,
            },
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        }
        ticket = fl.Ticket(json.dumps(query))
        return self._get_client().do_get(ticket).read_all()

    def get_event_frames(
        self,
        start_date: datetime = None,
        end_date: datetime = None,
        frame_type: str = None,
        selector: SeriesSelector = None,
    ):
        """Get all event frames matching the given criteria.

        Args:
            start_date: the start date of the range to find overlapping event frames in. Defaults to one year ago.
            end_date: the end date of the range to find overlapping event frames in. Defaults to now.
            frame_type: the type of event frames to search for. Finds all types when empty.
            selector: the time series source or time series to which the event frames are linked.
                Matches all by default.

        Returns::
            A pyarrow Table with 5 columns.
            The first column ('start_date') contains the start date.
            The second column ('end_date') contains the end date.
            The third column ('type') contains the type of the returned event frame as a string.
            Columns 4 ('series_source') and 5 ('series_name') contain the source and name of the series.
        """
        if start_date is None or end_date is None:
            now = datetime.utcnow().replace(tzinfo=timezone(timedelta(0)))
            if start_date is None:
                start_date = now.replace(year=now.year-1)
            if end_date is None:
                end_date = now

        query: Dict[str, Any] = {
            'query': 'get_event_frames',
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        }

        if frame_type is not None:
            query['type'] = frame_type
        if selector is not None:
            query['selector'] = {
                'source': selector.source,
            }
            if selector.name is not None:
                query['selector']['name'] = selector.name

        ticket = fl.Ticket(json.dumps(query))
        return self._get_client().do_get(ticket).read_all()

    def _get_client(self):
        if self._client is None:
            self._client = fl.FlightClient(self._location)
            if self._api_key != ('', ''):
                self._client.authenticate(ClientAuthenticationHandler(self._api_key))
        return self._client


def _read_metadata(data: Dict[str, Any]) -> Metadata:
    series = SeriesSelector(data['series']['source'], data['series']['name'])
    metadata = Metadata(series)
    for k, v in data.items():
        if v is None:
            continue
        if k == 'dictionary':
            metadata.set_field(k, Dictionary(dict(v)))
            continue
        metadata.set_field(k, v)
    return metadata


class ClientAuthenticationHandler(fl.ClientAuthHandler):
    """Client authentication handler for api keys"""
    def __init__(self, api_key):
        super().__init__()
        self.basic_auth = fl.BasicAuth(*api_key)
        self.token = None

    def authenticate(self, outgoing, incoming):
        """Client - server handshake"""
        auth = self.basic_auth.serialize()
        outgoing.write(auth)
        self.token = incoming.read()

    def get_token(self):
        """Get the token"""
        return self.token


def filter_series(
        series,
        event_frames,
):
    """Filter the even_frames out of the series.

        Args:
            series: a pyarrow table or a pandas Dataframe with a series.
            event_frames: pyarrow table or a pandas Dataframe with event frames.

        Returns::
            A filtered pyarrow table or a pandas Dataframe with 2 columns: 'ts' and 'value'.
    """
    if(HAS_PANDAS and isinstance(series, pd.DataFrame) and isinstance(event_frames, pd.DataFrame)):
        return filters_pandas.filter_series(series, event_frames)
    return filters_arrow.filter_series(series, event_frames)


def filter_event_frames(
        event_frames,
        start_date: datetime,
        end_date: datetime
):
    """Restrict time range to filter event frames.

        Args:
            event_frames: a pyarrow table or a pandas Dataframe with event frames.
            start_date: the start date of the range to filter event_frames.
            end_date: the end date of the range to filter event_frames.

        Returns::
            A filteredpyarrow table or a pandas Dataframe with 5 columns.
            The first column ('start_date') contains the 'start_date' and 'end_date'.
            The second column ('end_date') contains the 'end_date'.
            The third column ('type') contains the type of the returned event frame as a string.
            Columns 4 ('series_source') and 5 ('series_name') contain the source and name of the series.
    """
    if(HAS_PANDAS and isinstance(event_frames, pd.DataFrame)):
        return filters_pandas.filter_event_frames(event_frames, start_date, end_date)
    return filters_arrow.filter_event_frames(event_frames, start_date, end_date)
