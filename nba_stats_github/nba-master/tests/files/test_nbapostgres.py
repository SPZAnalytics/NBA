from __future__ import absolute_import

import logging
import unittest

from nba.db.pgsql import NBAPostgres


class NBAPostgres_test(unittest.TestCase):

    # changed NBAMongo class to require passing a db object
    # this allows testing using ming in-memory instance
    # still need a better way of having test data, probably should just pickle some examples and load them in tests

    def setUp(self):
        self.db = NBAPostgres()

    def test_init(self):
        nbapg = NBAPostgres()

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
