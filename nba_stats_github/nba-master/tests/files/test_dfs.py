from __future__ import absolute_import

import unittest

from nba.dfs import *


class NBADfs_test(unittest.TestCase):

    def test_dk_points(self):

        player = {
            'pts': 10,
            'fg3m': 0,
            'reb': 5,
            'ast': 4,
            'stl': 0,
            'blk': 0,
            'tov': 0
        }

        expected_points = 22.25
        self.assertEqual(dk_points(player), expected_points)

        player = {
            'pts': 10,
            'fg3m': 0,
            'reb': 10,
            'ast': 0,
            'stl': 0,
            'blk': 0,
            'tov': 0
        }

        expected_points = 24
        self.assertEqual(dk_points(player), expected_points)

        player = {
            'pts': 10,
            'fg3m': 0,
            'reb': 0,
            'ast': 10,
            'stl': 10,
            'blk': 0,
            'tov': 0
        }

        expected_points = 48
        self.assertEqual(dk_points(player), expected_points)


if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()