import json
from datetime import datetime, timedelta
import logging
from urllib import parse
import urllib3
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from ciso8601 import parse_datetime
import numpy as np

from dms_influx.decorators import runtime
from dms_influx.functions import downsample_indexes
from dms_influx.query import QueryString

logger = logging.getLogger(__name__)


class InfluxData(InfluxDBClient, QueryString):
    def __init__(self, database=None, trash_database=None, host: str = None, port: int = None,
                 username: str = None, password: str = None):

        if database is None:
            raise ValueError('Database must be set')

        self._database = database
        self._trash_database = f'trash_{database}' if trash_database is None else trash_database

        self.host = 'localhost' if host is None else host
        self.port = 8086 if port is None else port

        self.query_str = None

        try:
            super().__init__(host=self.host, port=self.port, username=username, password=password,
                             database=self._database)
            version = self.ping()
            self.create_database(self._database)
            logger.debug(f'Connected to influxdb, using database:{self._database}, version:{version}')
        except Exception as e:
            logger.error(f'Cannot connect to influxdb, e:{e}')
            raise

    @runtime
    def fetch_series_from_api(self, query=None, influx_client=False) -> dict:
        """Fetch series from influxdb api based on sql query

        :param query: Sql query to fetch
        :param influx_client: User influx client or no. Most of the time it is slower than urllib3 (bug?)
        """

        if query is None or query is "":
            raise ValueError("Query must not be None. Don't forget"
                             " to build queries with method `build_queries`")

        self.query_str = query

        if influx_client:
            return self.query(query).raw['series']

        url = f"http://{self.host}:{self.port}/query?"
        url = url + parse.urlencode({'db': self._database, 'q': query})
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        data = json.loads(response.data.decode('utf-8'))['results'][0]
        return data.get('series', [])

    @runtime
    def __transform_series(self, series, downsample=True, downsample_len=80000):
        """ Get series from data and downsample it

        :param downsample: Downsample to
        """

        series_out = []
        for item in series:
            tags = item.pop('tags')
            columns = item.pop('columns')
            ix_unit = columns.index('unit') if 'unit' in columns else None
            ix_ts = columns.index('time')
            ix_val = columns.index('value')
            # Take last item from values as a unit.
            if ix_unit is not None:
                item['unit'] = item['values'][-1][ix_unit]
                item['values'] = [(i[ix_ts], i[ix_val]) for i in item['values']]
            if downsample and len(item['values']) > downsample_len:
                item['values'] = self.downsample(item['values'], len_total=downsample_len)
            series_out.append({**item, **tags})
        return series_out

    def get_measurements(self) -> list:
        """Get list of measurements"""

        data = self.get_list_measurements()
        return [i['name'] for i in data]

    def __get_tags_list(self, tag=None) -> list:
        """Get list of tags"""

        tags = []
        self.build_queries(measurements='all', tag=tag)
        query = self.query_show_tags
        data = self.fetch_series_from_api(query=query, influx_client=False)
        for item in data:
            tags += [i[1] for i in item['values']]
        return tags

    @runtime
    def data_count(self, measurements=None, device_ids=None, combine=True, **kwargs):
        """Count all data """

        self.build_queries(measurements=measurements, device_ids=device_ids, **kwargs)
        query = self.query_count
        data = self.fetch_series_from_api(query=query, influx_client=True)
        data = self.__transform_series(data, downsample=False)
        if combine:
            data = {'count': sum([i['values'][0][1] for i in data])}
        else:
            for item in data:
                item['count'] = item['values'][0][1]
                del item['values']
        return data

    @runtime
    def save_data(self, data=None):
        """ Save data to database

        sample_data = [{
            id: <device_id>,
            device: <device_name>,
            channel: <channel>,
            unit: <unit>,
            values: [[ <utctime>, value], ...]
        }]

        :param data: Data to save
        """

        if type(data) == dict:
            data = [data]

        points = []
        for item in data:
            if not item['device_id']:
                raise ValueError('Device id must be supplied')
            device_id = item['device_id']
            measurement = item.get('measurement', device_id.split('.')[0])
            device = item.get('device', measurement)
            channel = item.get('channel', device_id.split('.')[1])
            unit = item.get('unit', '')
            for point in item['values']:
                if type(point) not in [list, tuple]:
                    raise ValueError('Point must be `tuple` or `list` example: (2021-01-01 00:00:00, 1)')

                ts = point[0]
                value = float(point[1])

                if type(ts) == datetime:
                    ts = str(ts)

                # Check if string is a valid timestamp
                try:
                    ts = parse_datetime(ts)
                except Exception:
                    raise ValueError('Time is not a valid string')
                #
                # if not utc:
                #     # Convert timestamp to UTC
                #     ts = self.tz.localize(ts)
                #     ts = ts.astimezone(pytz.utc)

                points.append({
                    "measurement": measurement,
                    "tags": {
                        "device_id": device_id,
                        "device": device,
                        "channel": channel,
                        "unit": unit,
                    },
                    "time": str(ts),
                    "fields": {
                        "value": value
                    }
                })

        self.write_points(points, batch_size=10000)

    def get_devices(self) -> list:
        """Get list of all devices"""

        return self.__get_tags_list(tag='device')

    def get_devices_ids(self) -> list:
        """Get list of all device_ids"""

        return self.__get_tags_list(tag='device_id')

    def get_unit(self, measurement, device_id) -> str:
        data = self.get_latest_data(measurements=measurement, device_ids=device_id)
        return data[0]['unit'] if len(data) >= 0 else None

    @runtime
    def get_latest_data(self, measurements=None, device_ids=None, **kwargs) -> list:
        """Get latest data from measurements
        :param device_ids:
        :param measurements: List or string of measurements
        :return: list of dicts of data; fields: name, columns, values, id, unit, channel, device
        """

        self.build_queries(measurements=measurements, device_ids=device_ids, order='desc', limit=1)
        query = self.query_select
        data = self.fetch_series_from_api(query=query, influx_client=True)
        data = self.__transform_series(data)
        return data

    @staticmethod
    def downsample(values=None, len_total=80000):
        # Downsample data to end length.

        if len(values) < len_total:
            return values

        y = np.array([i[1] for i in values])
        ix = downsample_indexes(y, len_total)
        return [values[i] for i in ix]

    @runtime
    def get_data(self, measurements=None, device_ids=None, downsample=True, mean=False, influx_client=False,
                 **kwargs) -> list:
        """ Get data from database

        :param influx_client:
        :param device_ids:
        :param measurements: Name of measurements
        :param downsample: Downsample data to smaller dataset (100k points)
        :param mean: Fetch mean values from database. Use `mean_interval` to set interval
        :param kwargs: Params to build QueryString
        :return: data = [{
            name: <measurement name>,
            id: <device id>,
            device: <device>,
            unit: <unit>,
            columns: [time, value (or mean_value)],
            channel: <channel>,
            values: <[[time,value],...]>
        }]
        """

        time = kwargs.pop('time', None)
        time_from = kwargs.pop('time_from', None)
        time_to = kwargs.pop('time_to', None)
        if time is not None:
            # Microseconds of the timestamp is different in python, hack to fetch range = -100us + 100us
            if type(time) is not datetime:
                time = parse_datetime(time)
            if time.microsecond > 100:
                time_from = time - timedelta(microseconds=100)
                time_to = time + timedelta(microseconds=100)
                time = None

        # Build query
        self.build_queries(measurements=measurements, device_ids=device_ids,
                           time=time, time_from=time_from, time_to=time_to, **kwargs)
        query = self.query_select_mean if mean else self.query_select
        series = self.fetch_series_from_api(query, influx_client=influx_client)
        # Get total length of fetched values
        values_len = sum([len(i["values"]) for i in series]) if series else 0
        data = self.__transform_series(series, downsample=downsample)
        if mean:
            for item in data:
                item['unit'] = self.get_unit(measurement=item['name'], device_id=item['device_id'])
        fetched_device_ids = [i['device_id'] for i in data] if data else None
        logger.info(f'Fetched measurements:{list(dict.fromkeys(i["name"] for i in data))}, '
                    f'device_ids:{fetched_device_ids}, series:{len(series)}, total values:{values_len}')
        return data

    @runtime
    def get_chart_data(self, measurements=None, device_ids=None, mean=False, **kwargs):
        """ Get data from database

        :param measurements: Name of measurements
        :param mean: Fetch mean values from database. Use `mean_interval` to set interval
        :param kwargs: Params to build QueryString
        :return: data = [{
            name: <measurement name>,
            device_id: <device id>,
            device: <device>,
            unit: <unit>,
            columns: [time, value (or mean_value)],
            channel: <channel>,
            x: <[time,...]>,
            y: <[value,...]>,
        }]
        """

        data = self.get_data(measurements=measurements, device_ids=device_ids, mean=mean, **kwargs)
        plotly_data = []
        for item in data:
            if item['values']:
                x, y = zip(*item['values'])
            else:
                x, y = [], []
            item['x'] = x
            item['y'] = y
            del item['values']
            plotly_data.append(item)
        data = plotly_data
        return data

    @runtime
    def __move_data(self, from_database, to_database, measurement=None, device_ids=None,
                    retention_duration='365d', set_retention=False, retention_name='trash',
                    delete_afterwords=True, **kwargs):
        """Copy data to from <from_database> to <to_database>"""

        self.switch_database(from_database)

        moved = {}

        self.create_database(to_database)

        if set_retention:
            self.create_retention_policy(name=retention_name, default=True, database=to_database,
                                                duration=retention_duration, replication='1')

        if measurement is None:
            raise TypeError('Argument `measurement` cannot be none')

        if type(measurement) == list:
            raise TypeError('Argument `measurement` cannot be type list')

        self.build_queries(measurements=measurement, device_ids=device_ids, select_into_database=to_database, **kwargs)
        query = self.query_copy
        try:
            data = self.fetch_series_from_api(query, influx_client=True)
            moved['copied'] = data[0]['values'][0][1]
        except InfluxDBClientError as e:
            # If data is older than set retention policy it will get dropped immediately. This cannot be reversed
            try:
                moved['dropped'] = str(e).split('dropped=')[1]
            except IndexError:
                # Invalid parsing
                moved['dropped'] = 'error'

        if delete_afterwords:
            # delete measurement from database
            query = self.query_delete
            self.fetch_series_from_api(query, influx_client=True)

        return moved

    @runtime
    def move_to_trash(self, measurement=None, device_ids=None, retention_duration='365d',
                      time=None, time_from=None, time_to=None, time_range=None, **kwargs) -> dict:
        """Move data to <trash> database and set retention policy"""

        return self.__move_data(from_database=self._database, to_database=self._trash_database,
                                measurement=measurement, device_ids=device_ids,
                                time=time, time_from=time_from, time_to=time_to, time_range=time_range,
                                retention_duration=retention_duration, set_retention=True, delete_afterwords=True,
                                **kwargs)

    def restore_from_trash(self, measurement=None, device_ids=None,
                           time=None, time_from=None, time_to=None, time_range=None, **kwargs):
        """Restore from data from <trash_database>"""

        return self.__move_data(from_database=self._trash_database, to_database=self._database,
                                measurement=measurement, device_ids=device_ids,
                                time=time, time_from=time_from, time_to=time_to, time_range=time_range,
                                set_retention=False, delete_afterwords=True, **kwargs)

    @runtime
    def delete_data(self, measurements=None, device_ids=None, time=None, time_from=None, time_to=None, time_range=None):
        """Delete data from database
        :param time_range:
        :param time_to:
        :param time_from:
        :param time:
        :param device_ids:
        :param measurements: Name of measurements
        """

        self.build_queries(measurements=measurements, device_ids=device_ids,
                           time=time, time_from=time_from, time_to=time_to, time_range=time_range)
        query = self.query_delete
        self.fetch_series_from_api(query, influx_client=True)
