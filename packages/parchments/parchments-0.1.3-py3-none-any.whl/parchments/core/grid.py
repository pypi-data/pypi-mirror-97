from parchments.core.row import Row
from parchments.core.period import Period
from parchments.core.choices import PERIOD_ITERATION_CHOICES, OVER_PERIOD_ITERATION_CHOICES
import json


class Grid:

    def __init__(self, row_index, period_iteration='month', over_period_iteration='year'):
        if period_iteration in PERIOD_ITERATION_CHOICES:
            self.period_iteration = period_iteration
        else:
            raise SyntaxError('Invalid period iteration choices %s' % PERIOD_ITERATION_CHOICES)

        if over_period_iteration in OVER_PERIOD_ITERATION_CHOICES:
            self.over_period_iteration = over_period_iteration
        else:
            raise SyntaxError('Invalid layer iteration choices %s' % OVER_PERIOD_ITERATION_CHOICES)

        self.row_index = row_index
        self.row_dict = dict()

        self.column_index = list()
        self.column_dict = dict()

        for row in self.row_index:
            self.row_dict[row[0]] = Row(row[0], row[1], row[2], self.period_iteration, self.over_period_iteration)

    def add_period(self, datetime, value_list, actual_value=True):
        period = Period(datetime, self.period_iteration)

        self.column_index.append(period)
        self.column_index.sort()
        self.column_dict[period.key] = period

        if type(value_list) is list:
            for loop_index, row in enumerate(self.row_index):
                self.row_dict[row[0]].add_block(period, value_list[loop_index], actual_value)

    def get_period_value_list(self, period):
        value_list = list()

        for row in self.row_index:
            value_list.append(self.row_dict[row[0]].get_block(period.key).data_dict['value'].raw)

        return value_list

    def as_dict(self, verbose_only=False, sum=True, average=True, json_dump=False):
        grid_dict = dict()
        grid_dict['column_data'] = list()

        for column in self.column_index:
            grid_dict['column_data'].append(self.column_dict[column.key].as_dict(verbose_only, json_dump=json_dump))

        grid_dict['row_data'] = dict()

        for row in self.row_index:
            grid_dict['row_data'][row[0]] = self.row_dict[row[0]].as_dict(verbose_only, sum, average)

        return grid_dict

    def as_list(self, verbose_only=False):
        grid_list = list()
        grid_list.append(self.column_index)

        for row in self.row_index:
            grid_list.append(self.row_dict[row[0]].as_list())

        return grid_list

    def as_json(self, verbose_only=False):
        return json.dumps(self.as_dict(verbose_only, json_dump=True))

    def as_html(self):
        pass

    def get_row(self, row_index_key):
        if row_index_key in list(self.row_dict.keys()):
            return self.row_dict[row_index_key]
        else:
            raise ValueError('Invalid row index. Your choices are %s' % list(self.row_dict.keys()))

    def get_block(self, row_index_key, datetime):
        period = Period(datetime, self.period_iteration)

        if row_index_key in list(self.row_dict.keys()):
            return self.row_dict[row_index_key].get_block(period.key)
        else:
            raise ValueError('Invalid row index. Your choices are %s' % list(self.row_dict.keys()))

    def project_missing_period(self, period, column_index, method='linear'):
        if period.next_period not in column_index:
            if method == 'linear':
                self.add_period(period.next_period.data_dict['datetime'], self.get_period_value_list(period), False)
                self.project_missing_period(period.next_period, column_index, method)

    def project_missing(self, method='linear'):
        column_index = list(self.column_index)
        for index, column in enumerate(column_index):
            if index < len(column_index) - 1:
                self.project_missing_period(column, column_index)

    def project_future(self, period_datetime, method='linear'):
        latest_period = self.column_index[len(self.column_index) - 1]
        while latest_period < Period(period_datetime, self.period_iteration):
            self.add_period(latest_period.next_period.data_dict['datetime'], self.get_period_value_list(latest_period), False)
            latest_period = latest_period.next_period

    def project_past(self, period_datetime, method='linear'):
        earliest_period = self.column_index[0]
        while earliest_period > Period(period_datetime, self.period_iteration):
            self.add_period(earliest_period.previous_period.data_dict['datetime'], self.get_period_value_list(earliest_period), False)
            earliest_period = earliest_period.previous_period
