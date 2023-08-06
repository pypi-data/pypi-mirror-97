from parchments.core.value import Value
import decimal
import json


class Block:

    def __init__(self, period, value, value_type: str, decimal_places=0, actual_value=True):
        self.period = period
        self.value = value
        self.value_type = value_type
        self.decimal_places = decimal_places
        self.actual_value = actual_value
        self.data_dict = {
            'actual_value': self.actual_value,
            'period_key': self.period.key,
        }
        self.add_value('value', value)

    def as_dict(self, verbose_only=False, json_dump=False):
        block_dict = dict()
        for key, val in self.data_dict.items():
            if type(val) is Value:
                block_dict[key] = val.as_dict(verbose_only)
            else:
                block_dict[key] = val
        return block_dict

    def as_list(self, verbose_only=False):
        block_list = list()
        for key, val in self.data_dict.items():
            if type(val) is Value:
                block_list.append(val.as_list())
            else:
                block_list.append(val)
        return block_list

    def as_json(self, verbose_only=False):
        return json.dumps(self.as_dict(verbose_only))

    def compare_historical(self, historical_block):
        if self.value_type not in ('string', 'bool'):
            self.add_value('growth_amount', self.value - historical_block.value)
            try:
                self.add_value('growth_percentage', self.get_value('growth_amount').raw / historical_block.get_value('value').raw, 'percentage', 4)
            except (ZeroDivisionError, decimal.DecimalException) as error:
                self.add_value('growth_percentage', 0)

    def compare_over_historical(self, over_historical_block):
        if self.value_type not in ('string', 'bool'):
            self.add_value('over_growth_amount', self.value - over_historical_block.value)
            try:
                self.add_value('over_growth_percentage', self.get_value('over_growth_amount').raw / over_historical_block.get_value('value').raw, 'percentage', 4)
            except (ZeroDivisionError, decimal.DecimalException) as error:
                self.add_value('over_growth_percentage', 0)

    def calculate_growth(self, value1, value2):
        pass

    def add_value(self, name, value, value_type=None, decimal_places=None):
        if value_type is None:
            value_type = self.value_type
        if decimal_places is None:
            decimal_places = self.decimal_places
        self.data_dict[name] = Value(value, value_type, decimal_places)

    def get_value(self, name):
        return self.data_dict[name]