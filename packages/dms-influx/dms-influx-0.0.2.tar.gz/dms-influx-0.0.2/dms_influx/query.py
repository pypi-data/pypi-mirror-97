from dateutil.parser import parse
from datetime import datetime
from time import localtime

class QueryString:
    def __init__(self):
        self.query_select = None
        self.query_select_last = None
        self.query_select_last_grouped = None
        self.query_select_mean = None
        self.query_delete = None
        self.query_copy = None
        self.query_count = None
        self.query_show_tags = None

        print ('what')

        super().__init__()

    def build_queries(self,
                      measurements=None,
                      device_ids=None,
                      time=None,
                      time_from=None,
                      time_to=None,
                      time_range=None,
                      value=None,
                      limit=None,
                      mean_interval='1h',
                      select_into_database='trash',
                      tag=None,
                      order='asc',
                      values_above=None,
                      values_below=None,
                      not_values=None,
                      ):
        """

        :param measurements:
        :param device_ids:
        :param time:
        :param time_from:
        :param time_to:
        :param time_range:
        :param value:
        :param limit:
        :param mean_interval:
        :param select_into_database:
        :param tag:
        :param order:
        :param values_above:
        :param values_below:
        :param not_values:
        :return:
        """

        def __flt_q(query):
            return 'and' if 'where' in query else 'where'

        measurements = measurements if measurements is not None else 'all'
        measurements = [measurements] if type(measurements)==str else measurements

        q_meas = '/.*/' if 'all' in measurements else (', '.join('"' + item + '"' for item in measurements))

        q_device_ids = ""
        if device_ids:
            if device_ids and type(device_ids) == str:
                device_ids = [device_ids]
            for i, device_id in enumerate(device_ids):
                if i == 0:
                    q_device_ids += f"device_id='{device_id}'"
                else:
                    q_device_ids += f" or device_id='{device_id}'"

        q_time_range = ""
        if time_range is not None:
            utc_offset = localtime().tm_gmtoff // 60
            offset_str = f"+ {utc_offset}" if utc_offset >= 0 else f"- {utc_offset}"
            q_time_range = f'time > now() {offset_str}m - {time_range}'

        q_time = ""
        if time is not None:
            try:
                # If the argument is only year
                time = str(datetime.strptime(time, '%Y'))
            except:
                pass
            if type(time) == datetime:
                time = str(time)
            q_time = f"time = '{str(parse(time))}'"

        q_time_from = ""
        if time_from is not None:
            try:
                # If the argument is only year
                time_from = str(datetime.strptime(time_from, '%Y'))
            except:
                pass
            if type(time_from) == datetime:
                time_from = str(time_from)
            q_time_from = f"time >= '{str(parse(time_from))}'"

        q_time_to = ""
        if time_to is not None:
            try:
                # If the argument is only year
                time_to = str(datetime.strptime(time_to, '%Y'))
            except:
                pass
            if type(time_to) == datetime:
                time_to = str(time_to)
            q_time_to = f"time <= '{str(parse(time_to))}'"

        q_value = ""
        if value is not None:
            q_value = f'value = {value}'

        q_values_above = ""
        if values_above is not None:
            values_above = list(values_above) if type(values_above) is not list else values_above
            q_values_above = ' and '.join([f'value > {i}' for i in values_above])

        q_values_below = ""
        if values_below is not None:
            values_below = list(values_below) if type(values_below) is not list else values_below
            q_values_below = ' and '.join([f'value < {i}' for i in values_below])

        q_not_values = ""
        if not_values is not None:
            not_values = list(not_values) if type(not_values) is not list else not_values
            q_not_values = ' and '.join([f'value != {i}' for i in not_values])


        q_conditions = ""
        if q_device_ids:
            q_conditions += f" {__flt_q(q_conditions)} {q_device_ids}"
        if q_time_range:
            q_conditions += f" {__flt_q(q_conditions)} {q_time_range}"
        if q_time_from:
            q_conditions += f" {__flt_q(q_conditions)} {q_time_from}"
        if q_time_to:
            q_conditions += f" {__flt_q(q_conditions)} {q_time_to}"
        if q_time:
            q_conditions += f" {__flt_q(q_conditions)} {q_time}"
        if q_value:
            q_conditions += f" {__flt_q(q_conditions)} {q_value}"
        if q_values_above:
            q_conditions += f" {__flt_q(q_conditions)} {q_values_above}"
        if q_values_below:
            q_conditions += f" {__flt_q(q_conditions)} {q_values_below}"
        if q_not_values:
            q_conditions += f" {__flt_q(q_conditions)} {q_not_values}"

        # Add limit
        q_limit = f"limit {limit}" if limit else ""
        q_order = f'order by time {order}'

        q_group_by = 'device_id, channel, device'
        q_select = 'time, value, unit'

        # Build queries

        self.query_select = f'select {q_select} from {q_meas} {q_conditions} group by {q_group_by}  {q_order} {q_limit}'
        self.query_select_mean = f'select round(mean(value)*100)/100 as value from {q_meas} {q_conditions} ' \
                                 f'group by time({mean_interval}), {q_group_by} fill(none) {q_order} {q_limit}'

        # self.query_select_last = f'select last(value) as value from {q_meas} {q_conditions} {q_limit}'
        # self.query_select_last_grouped = f'select last(value) as value from {q_meas} {q_conditions}' \
        #                                  f'group by {q_group_by} {q_limit}'
        # self.query_select_last = f'select time, value, unit from {q_meas} {q_conditions} group by {q_group_by} ' \
        #                          f'order by time desc 1'

        self.query_copy = f'select * into "{select_into_database}"..{q_meas} from {q_meas} {q_conditions}' \
                          f'group by * {q_order} {q_limit}'
        self.query_count = f'select count(value) as value from {q_meas} {q_conditions} group by {q_group_by} {q_order} {q_limit}'
        self.query_delete = f'delete from {q_meas} {q_conditions}'
        self.query_show_tags = f'show tag values from {q_meas} with key="{tag}" {q_conditions} {q_limit}'



