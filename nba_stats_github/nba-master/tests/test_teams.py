from __future__ import absolute_import

import unittest

from nba.teams import NBATeamNames


class NBATeams_test(unittest.TestCase):

    def setUp(self):
        self.teams = NBATeamNames()

    def test_city_to_code(self):
        self.assertEqual(self.teams.city_to_code('Chicago'), 'CHI')

    def test_long_to_code(self):
        self.assertEqual(self.teams.long_to_code('Chicago Bulls'), 'CHI')

    def test_id_to_code(self):
        self.assertEqual(self.teams.id_to_code('1610612741'), 'CHI')

    def test_code_to_id(self):
        self.assertEqual(self.teams.code_to_id('CHI'), '1610612741')

    def test_code_to_long(self):
        self.assertEqual(self.teams.code_to_long('CHI'), 'Chicago Bulls')

if __name__=='__main__':
    unittest.main()