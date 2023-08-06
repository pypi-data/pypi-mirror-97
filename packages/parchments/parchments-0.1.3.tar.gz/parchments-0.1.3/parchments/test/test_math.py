import unittest
import parchments
import datetime
import decimal

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

test_grid = parchments.Grid(TEST_INDEX)
test_grid.add_period(datetime.datetime(2020, 4, 1), PERIOD_DATA)
test_grid.add_period(datetime.datetime(2020, 5, 1), OTHER_PERIOD_DATA)
test_grid.add_period(datetime.datetime(2020, 6, 1), MORE_PERIOD_DATA)


class TestMath(unittest.TestCase):

    def test_row_sum(self):
        self.assertTrue(test_grid.as_dict()['row_data']['goats'][3]['sum']['raw'] == 600)

    def test_row_average(self):
        self.assertTrue(test_grid.as_dict()['row_data']['goats'][4]['average']['raw'] == 200)