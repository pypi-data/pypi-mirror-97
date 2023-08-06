from decimal import Decimal
import json


class Value:

    def __init__(self, value, value_type, decimals=2):
        self.data_dict = {
            'raw': value,
            'type': value_type,
            'decimals': decimals,
        }
        self.update()

    def __truediv__(self, other):
        return self.data_dict['raw'] / other.data_dict['raw']

    def __idiv__(self, other):
        self.data_dict['raw'] = self.__truediv__(other)
        self.update()
        return self

    def __mul__(self, other):
        return self.data_dict['raw'] * other.data_dict['raw']

    def __imul__(self, other):
        self.data_dict['raw'] = self.__mul__(other)
        self.update()
        return self

    def __add__(self, other):
        return self.data_dict['raw'] + other.data_dict['raw']

    def __iadd__(self, other):
        self.data_dict['raw'] = self.__add__(other)
        self.update()
        return self

    def __sub__(self, other):
        return self.data_dict['raw'] - other.data_dict['raw']

    def __isub__(self, other):
        self.data_dict['raw'] = self.__sub__(other)
        self.update()

    def update(self):
        self.clean()
        self.verbose()

    def clean(self):
        if type(self.data_dict['type']) == 'dollar' or type(self.data_dict['type']) == 'percentage':
            self.data_dict['clean'] = round(self.data_dict['raw'], self.data_dict['decimals'])
        else:
            self.data_dict['clean'] = self.data_dict['raw']

    def verbose(self):
        if self.data_dict['raw'] in (0, 0.0, Decimal(0.0)):
            self.data_dict['verbose'] = '-'
        elif self.data_dict['type'] == 'dollar':
            self.data_dict['verbose'] = '${:,.{}f}'.format(self.data_dict['raw'], self.data_dict['decimals'])
        elif self.data_dict['type'] == 'percentage':
            self.data_dict['verbose'] = '{:,.{}f}%'.format((self.data_dict['raw'] * 100), self.data_dict['decimals'])
        elif self.data_dict['type'] == 'int':
            self.data_dict['verbose'] = '{:,.{}f}'.format(self.data_dict['raw'], self.data_dict['decimals'])
        elif self.data_dict['type'] == 'bool':
            if self.data_dict['raw']:
                self.data_dict['verbose'] = 'True'
            else:
                self.data_dict['verbose'] = 'False'
        elif self.data_dict['type'] == 'string':
            self.data_dict['verbose'] = self.data_dict['raw']

    def as_dict(self, verbose_only=False, json_dump=False):
        if verbose_only:
            return {
                'verbose': self.data_dict['verbose'],
            }
        else:
            return self.data_dict

    def as_list(self, verbose_only=False):
        value_list = list()
        for key, val in self.data_dict.items():
            value_list.append(val)
        return value_list

    def as_json(self, verbose_only=False):
        return json.dumps(self.as_dict(verbose_only))

    @property
    def raw(self):
        return self.data_dict['raw']
