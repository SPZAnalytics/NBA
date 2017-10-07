'''
playerprofiler_scraper_test.py
'''

import json
import unittest

from nfl.scrapers.playerprofiler import PlayerProfilerNFLScraper

class TestPlayerProfilerScraper(unittest.TestCase):

    def setUp(self):
        self.s = PlayerProfilerNFLScraper()

    def test_player_page(self):
        content = self.s.player_page('TT-0500')
        self.assertIsNotNone(content)
        data = json.loads(content)
        self.assertIsInstance(data, dict)

    def test_players(self):
        content = self.s.players()
        self.assertIsNotNone(content)
        data = json.loads(content)
        self.assertIsInstance(data, dict)

    def test_rankings(self):
        content = self.s.rankings()
        self.assertIsNotNone(content)
        data = json.loads(content)
        self.assertIsInstance(data, dict)

if __name__ == '__main__':
    unittest.main()