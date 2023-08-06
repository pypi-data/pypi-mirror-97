import unittest
import parchments
import datetime
import decimal
import json

TEST_INDEX = (
    ('goats', 'int', 0),
    ('price', 'dollar', 2),
    ('value', 'percentage', 4),
    ('names', 'string', 0),
    ('animal', 'bool', 0),
)

test_grid = parchments.Grid(TEST_INDEX)


class TestGrid(unittest.TestCase):

    def test_grid_add_period(self, period=datetime.datetime.now(), index=[1, 22.2, 0.70, 'bob', True]):
        try:
            test_grid.add_period(datetime.datetime.now(), [1, 22.2, 0.70, 'bob', True])
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_add_period_with_datetime_input(self):
        self.test_grid_add_period(period=datetime.datetime.now())

    def test_add_period_with_date_input(self):
        self.test_grid_add_period(period=datetime.date.today())

    def test_add_period_with_decimal_input(self):
        self.test_grid_add_period(index=[1, decimal.Decimal(22.2), 0.70, 'bob', True])

    def test_add_period_with_float_input(self):
        self.test_grid_add_period(index=[1, float(22.2), 0.70, 'bob', True])

    def test_add_period_with_zero_division_input(self):
        self.test_grid_add_period(index=[1, 22.0, 0.70, 'bob', True])
        self.test_grid_add_period(index=[1, 0.0, 0.70, 'bob', True])

    def test_grid_as_dict(self):
        try:
            self.assertTrue(type(test_grid.as_dict()) is dict)
        except:
            self.assertTrue(False)

    def test_grid_as_list(self):
        try:
            self.assertTrue(type(test_grid.as_list()) is list)
        except:
            self.assertTrue(False)

    def test_grid_as_json(self):
        try:
            self.assertTrue(json.loads(test_grid.as_json()))
        except:
            self.assertTrue(False)

    def test_grid_get_row(self):
        try:
            test_grid.get_row('goats')
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_grid_get_block(self):
        try:
            test_grid.get_block('goats', datetime.datetime.now())
            self.assertTrue(True)
        except:
            self.assertTrue(False)
