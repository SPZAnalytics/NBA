from __future__ import absolute_import

import logging
import random
import unittest

from nba.db.fantasylabs import FantasyLabsNBAPg


class NBAPostgres_test(unittest.TestCase):

    # changed NBAMongo class to require passing a db object
    # this allows testing using ming in-memory instance
    # still need a better way of having test data, probably should just pickle some examples and load them in tests

    def setUp(self):
        self.db = FantasyLabsNBAPg()

    def test_init(self):
        flpg = FantasyLabsNBAPg()

    def test_nbacom_player_id(self):
        '''
        Not sure what this does
        Returns:

        '''
        pass
        #flpg = FantasyLabsNBAPg()
        #site_player_ids = [12082, 12062, 12310, 12275, 12230, 12631, 12605, 12333, 12397, 12338, 12072, 12279, 12048, 12663, 12068, 12067, 12201, 12217, 12537, 12371, 12496, 12049, 12248, 12267, 12181, 12395, 12436, 12478, 12038, 12205, 12244, 12376, 12365, 12119, 12377, 12547, 12423, 12184, 12655, 12286, 12482, 12432, 12640, 12097, 12524, 12093, 12393, 12557, 12583, 12315, 12412, 12128, 12616, 12610, 12578, 12140, 12418, 12577, 12381, 12127, 12212, 12652, 12646, 12325, 12250, 12666, 12552, 12623, 12161, 12150, 12634, 12186, 12406, 12551, 12588, 12348, 12073, 12361, 12323, 12453, 12129, 12081, 12501, 12041, 12523, 12567, 12612, 12022, 12278, 12302, 12405, 12468, 12294]
        #nbacom_id = flpg._nbacom_player_id(random.choice(site_player_ids))
        #self.assertIsNotNone(nbacom_id, 'Should have value for nbacom_id')

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
