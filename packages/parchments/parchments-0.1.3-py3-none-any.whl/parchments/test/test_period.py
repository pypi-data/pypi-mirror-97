import unittest
import parchments
import datetime
import calendar

TEST_INDEX = (
    ('goats', 'int', 0),
    ('price', 'dollar', 2),
    ('value', 'percentage', 4),
    ('names', 'string', 0),
    ('animal', 'bool', 0),
)

PERIOD_DATA = [
    200,
    3000.00,
    0.7500,
    'goaty mc goaterson',
    True,
]

OTHER_PERIOD_DATA = [
    300,
    4000.00,
    0.5500,
    'douglas bahhhhh',
    True,
]

MORE_PERIOD_DATA = [
    100,
    2000.00,
    0.6500,
    'waaaaaaaaah sheep licker',
    False,
]


class TestPeriod(unittest.TestCase):

    def test_previous_period_year_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='year')
        period_test_grid.add_period(datetime.datetime(2020, 4, 1), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].previous_period.key == '20190101')

    def test_next_period_year_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='year')
        period_test_grid.add_period(datetime.datetime(2020, 4, 1), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].next_period.key == '20210101')

    def test_previous_period_month_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='month')
        period_test_grid.add_period(datetime.datetime(2020, 4, 1), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].previous_period.key == '20200301')

    def test_previous_period_year_roll_over_month_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='month')
        period_test_grid.add_period(datetime.datetime(2020, 1, 1), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].previous_period.key == '20191201')

    def test_next_period_month_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='month')
        period_test_grid.add_period(datetime.datetime(2020, 4, 1), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].next_period.key == '20200501')

    def test_next_period_year_roll_over_month_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='month')
        period_test_grid.add_period(datetime.datetime(2020, 12, 1), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].next_period.key == '20210101')

    def test_previous_period_day_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='day')
        period_test_grid.add_period(datetime.datetime(2020, 4, 10), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].previous_period.key == '20200409')

    def test_previous_period_month_roll_over_day_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='day')
        period_test_grid.add_period(datetime.datetime(2020, 4, 1), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].previous_period.key == '20200331')

    def test_previous_period_year_roll_over_day_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='day')
        period_test_grid.add_period(datetime.datetime(2020, 1, 1), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].previous_period.key == '20191231')

    def test_next_period_day_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='day')
        period_test_grid.add_period(datetime.datetime(2020, 4, 10), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].next_period.key == '20200411')

    def test_next_period_month_roll_over_day_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='day')
        period_test_grid.add_period(datetime.datetime(2020, 4, 30), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].next_period.key == '20200501')

    def test_next_period_year_roll_over_day_iteration(self):
        period_test_grid = parchments.Grid(TEST_INDEX, period_iteration='day')
        period_test_grid.add_period(datetime.datetime(2020, 12, 31), PERIOD_DATA)
        self.assertTrue(period_test_grid.column_index[0].next_period.key == '20210101')

