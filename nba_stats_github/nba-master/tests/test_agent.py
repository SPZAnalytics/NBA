from __future__ import absolute_import, print_function

import os
import unittest

from nba.agents.agent import NBAAgent


class NBAAgent_test(unittest.TestCase):

    def setUp(self):
        self.a = NBAAgent()

    def test_open_file_csv(self):
        fname = 'files/sampleDKSalaries.csv'
        data = self.a.read_file(fname)
        self.assertIsNotNone(data)
        self.assertTrue(len(data) > 0)

    def test_save_file_csv(self):
        fname = '/tmp/sample.csv'
        data = self.a.read_file('sample.csv')
        self.a.save_file(data, fname)
        self.assertTrue(os.path.exists(fname))

if __name__=='__main__':
    unittest.main()
