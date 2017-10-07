from __future__ import absolute_import

import datetime as dt
import unittest

from nba.dates import *


class NBADates_test(unittest.TestCase):

    def test_date_list(self):
        d1 = dt.datetime.today()
        d2 = d1 - dt.timedelta(7)
        dates = date_list(d1, d2)
        self.assertIn(d1, dates)
        self.assertIn(d2, dates)
        self.assertNotIn(d1 + dt.timedelta(3), dates)
        self.assertNotIn(d2 - dt.timedelta(3), dates)
        dates = date_list(d2, d1)
        self.assertEqual(len(dates), 0)

    def test_format_type(self):

        fmt = format_type('10_22_2015')
        self.assertEqual(fmt, site_format('fl'))

        fmt = format_type('2015-10-22')
        self.assertEqual(fmt, site_format('nba'))

        fmt = format_type('10-22-2015')
        self.assertEqual(fmt, site_format('std'))

if __name__=='__main__':
    unittest.main()