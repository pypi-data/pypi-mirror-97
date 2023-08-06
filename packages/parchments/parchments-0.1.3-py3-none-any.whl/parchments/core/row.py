from parchments.core.validation import is_valid_list_choice, is_valid_date_or_datetime
from parchments.core.block import Block
from parchments.core.value import Value
from parchments.core.choices import VALUE_TYPE_CHOICES
import json


class Row:

    def __init__(self, name, value_type, value_decimals, period_iteration, over_period_iteration):
        if is_valid_list_choice(value_type, VALUE_TYPE_CHOICES):
            self.value_type = value_type

        self.value_decimals = value_decimals
        self.name = name
        self.period_iteration = period_iteration
        self.over_period_iteration = over_period_iteration
        self.block_order_list = list()
        self.block_dict = dict()
        self.data_dict = dict()

    def add_block(self, period, value, actual_value=True):
        self.block_dict[period.key] = Block(period, value, self.value_type, self.value_decimals, actual_value)

        if period.key not in self.block_order_list:
            self.block_order_list.append(period.key)

        self.block_order_list.sort()

        self.update_sum_and_average(value)
        self.update()

    def update(self):
        for loop_index, block_order in enumerate(self.block_order_list):
            if loop_index == 0:
                self.block_dict[block_order].compare_historical(self.block_dict[block_order])
            else:
                self.block_dict[block_order].compare_historical(self.block_dict[self.block_order_list[loop_index - 1]])

            if self.over_period_iteration == 'year':
                if str(int(block_order) - 10000) in self.block_order_list:
                    self.block_dict[block_order].compare_over_historical(
                        self.block_dict[str(int(block_order) - 10000)])
                else:
                    self.block_dict[block_order].compare_over_historical(self.block_dict[block_order])

    def as_dict(self, verbose_only=False, sum=True, average=True, json_dump=False):
        row_list = list()

        for block_order in self.block_order_list:
            row_list.append(self.block_dict[block_order].as_dict(verbose_only, json_dump=json_dump))

        if sum:
            row_list.append({ 'sum': self.data_dict['sum'].as_dict(verbose_only, json_dump=json_dump) })

        if average:
            row_list.append({ 'average': self.data_dict['average'].as_dict(verbose_only, json_dump=json_dump) })

        return row_list

    def as_list(self, verbose_only=False):
        row_list = list()

        for block_order in self.block_order_list:
            row_list.append(self.block_dict[block_order].as_list())

        row_list.append(self.data_dict['sum'].as_list())

        return row_list

    def as_json(self, verbose_only=False):
        return json.dumps(self.as_dict(verbose_only, json_dump=True))

    def get_block(self, column_index):
        if column_index in self.block_order_list:
            return self.block_dict[column_index]
        else:
            raise ValueError('Invalid column index. Your choices are %s' % self.block_order_list)

    def update_sum_and_average(self, value):
        if 'sum' in self.data_dict:
            self.data_dict['sum'] += Value(value, self.value_type, self.value_decimals)
        else:
            self.data_dict['sum'] = Value(value, self.value_type, self.value_decimals)

        if self.value_type not in ('string', 'bool'):
            self.data_dict['average'] = Value(self.data_dict['sum'].as_dict()['raw'] / len(self.block_order_list), self.value_type, self.value_decimals)
        else:
            self.data_dict['average'] = Value('-', self.value_type, self.value_decimals)

