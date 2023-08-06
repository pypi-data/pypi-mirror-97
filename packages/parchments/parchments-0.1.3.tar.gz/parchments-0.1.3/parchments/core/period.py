from datetime import date, datetime
import json
from calendar import monthrange


class Period:

    def __init__(self, date_or_datetime, iteration):
        self.data_dict = dict()
        if type(date_or_datetime) is date:
            self.data_dict['date'] = date_or_datetime
            self.data_dict['datetime'] = datetime.combine(date_or_datetime, datetime.min.time())
        elif type(date_or_datetime is datetime):
            self.data_dict['date'] = date_or_datetime.date()
            self.data_dict['datetime'] = date_or_datetime
        else:
            raise ValueError('Invalid period. Must be a datetime.date or datetime.datetime')

        self.data_dict['iteration'] = iteration

        if self.data_dict['iteration'] == 'year':
            self.data_dict['key'] = self.data_dict['datetime'].strftime('%Y0101')
            self.data_dict['verbose'] = self.data_dict['datetime'].strftime('%Y')
            self.data_dict['verbose_numeric'] = self.data_dict['datetime'].strftime('%Y-01-01')
        if self.data_dict['iteration'] == 'month':
            self.data_dict['key'] = self.data_dict['datetime'].strftime('%Y%m01')
            self.data_dict['verbose'] = self.data_dict['datetime'].strftime('%b %Y')
            self.data_dict['verbose_numeric'] = self.data_dict['datetime'].strftime('%Y-%m-01')
        if self.data_dict['iteration'] == 'day':
            self.data_dict['key'] = self.data_dict['datetime'].strftime('%Y%m%d')
            self.data_dict['verbose'] = self.data_dict['datetime'].strftime('%b %d %Y')
            self.data_dict['verbose_numeric'] = self.data_dict['datetime'].strftime('%Y-%m-%d')

    def __eq__(self, other):
        return self.key_as_int() == other.key_as_int()

    def __ge__(self, other):
        return self.key_as_int() >= other.key_as_int()

    def __gt__(self, other):
        return self.key_as_int() > other.key_as_int()

    def __le__(self, other):
        return self.key_as_int() <= other.key_as_int()

    def __lt__(self, other):
        return self.key_as_int() < other.key_as_int()

    def __str__(self):
        return self.data_dict['key']

    @property
    def key(self):
        return self.data_dict['key']

    def key_as_int(self):
        return int(self.data_dict['key'])

    def as_dict(self, verbose_only=False, json_dump=False):
        if verbose_only:
            return {
                'verbose': self.data_dict['verbose'],
                'verbose_numeric': self.data_dict['verbose_numeric'],
            }
        elif json_dump:
            return {
                'key': self.data_dict['verbose'],
                'verbose': self.data_dict['verbose'],
                'verbose_numeric': self.data_dict['verbose_numeric'],
            }
        else:
            return self.data_dict

    def as_list(self, verbose_only=False):
        data_list = list()
        for key, val in self.data_dict.items():
            data_list.append(val)
        return data_list

    def as_json(self, verbose_only=False):
        return json.dumps(self.as_dict())

    def next_datetime(self):
        current_datetime = self.data_dict['datetime']
        if self.data_dict['iteration'] == 'year':
            return datetime(current_datetime.year + 1, current_datetime.month, 1)
        if self.data_dict['iteration'] == 'month':
            return datetime(current_datetime.year + int(current_datetime.month / 12), ((current_datetime.month % 12) + 1), 1)
        if self.data_dict['iteration'] == 'day':
            if current_datetime.day + 1 > monthrange(current_datetime.year, current_datetime.month)[
                    1] and current_datetime.month != 12:
                return datetime(current_datetime.year, current_datetime.month + 1, 1)
            elif current_datetime.day + 1 > monthrange(current_datetime.year, current_datetime.month)[
                    1] and current_datetime.month == 12:
                return datetime(current_datetime.year + 1, 1, 1)
            else:
                return datetime(current_datetime.year, current_datetime.month, current_datetime.day + 1)

    @property
    def next_period(self):
        return Period(self.next_datetime(), self.data_dict['iteration'])

    def previous_datetime(self):
        current_datetime = self.data_dict['datetime']
        if self.data_dict['iteration'] == 'year':
            return datetime(current_datetime.year - 1, current_datetime.month, 1)
        if self.data_dict['iteration'] == 'month':
            if current_datetime.month - 1 == 0:
                return datetime(current_datetime.year - 1, 12, 1)
            else:
                return datetime(current_datetime.year, current_datetime.month - 1, 1)
        if self.data_dict['iteration'] == 'day':
            if current_datetime.day - 1 == 0 and current_datetime.month == 1:
                return datetime(current_datetime.year - 1, 12, monthrange(current_datetime.year - 1, 12)[1])
            elif current_datetime.day - 1 == 0 and current_datetime.month != 1:
                return datetime(current_datetime.year, current_datetime.month - 1, monthrange(current_datetime.year - 1, 12)[1])
            else:
                return datetime(current_datetime.year, current_datetime.month, current_datetime.day - 1)

    @property
    def previous_period(self):
        return Period(self.previous_datetime(), self.data_dict['iteration'])

