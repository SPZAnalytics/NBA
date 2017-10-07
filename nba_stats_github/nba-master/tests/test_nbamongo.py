from __future__ import absolute_import

import logging
import unittest

import ming

from nba.db.mongo import NBAMongo

class NBAMongo_test(unittest.TestCase):

    # changed NBAMongo class to require passing a db object
    # this allows testing using ming in-memory instance
    # still need a better way of having test data, probably should just pickle some examples and load them in tests

    def setUp(self):
        #self.mg = ming.create_datastore('mim://', db='nba', **kwargs)
        #self.nbam = NBAMongo(self.mg.db)
        #self.games = []
        #self.standings = []
        #self._get_scoreboard()
        pass

    def test_add_games(self):
        #ids = self.nbam.add_games(self.games)
        #self.assertGreater(ids.count, 0, "should have some ids after insert")
        pass

    def test_get_games(self):
        #games = self.nbam.get_games()
        #self.assertGreater(games.count, 0, "should have some games after query")
        pass

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
