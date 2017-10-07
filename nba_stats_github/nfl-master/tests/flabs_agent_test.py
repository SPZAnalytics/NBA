import json
import logging
import unittest

import browsercookie

from nfl.agents.fantasylabs import FantasyLabsNFLAgent
from nfl.optimizers.orm import ORToolsRoster


class TestFantasyLabsNFLAgent(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

        with open('data/model.json') as infile:
            self.a = FantasyLabsNFLAgent(cache_name='data/testfantasylabs', cj=browsercookie.firefox())
            self.players = json.load(infile)

    def test_instantiate(self):
        self.assertIsInstance(self.a, FantasyLabsNFLAgent)

    def test_optimizer(self):
        for projform in ['cash', 'tourncash', 'tournament']:
            rosters = self.a.optimize(players=self.players, projection_formula=projform)
            self.assertGreater(len(rosters), 0, 'should have at least 1 roster')
            for id, roster in rosters.items():
                self.assertIsInstance(id, basestring)
                logging.debug('{} {}'.format(projform, id))
                self.assertIsInstance(roster, ORToolsRoster)
                logging.debug(roster)