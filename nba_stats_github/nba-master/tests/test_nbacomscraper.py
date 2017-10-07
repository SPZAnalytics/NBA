from __future__ import absolute_import

import logging
import unittest

from nba.scrapers.nbacom import NBAComScraper


class NBAComScraper_test(unittest.TestCase):

    def setUp(self):
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        self.nbs = NBAComScraper()

    def test_boxscore(self):
        box = self.nbs.boxscore_traditional('0021500001')
        self.assertIsInstance(box, dict)
        self.assertIsNotNone(box.get('resultSets', None))
        box = self.nbs.boxscore_advanced('0021500001')
        self.assertIsInstance(box, dict)
        self.assertIsNotNone(box.get('resultSets', None))
        box = self.nbs.boxscore_scoring('0021500001')
        self.assertIsInstance(box, dict)
        self.assertIsNotNone(box.get('resultSets', None))
        box = self.nbs.boxscore_misc('0021500001')
        self.assertIsInstance(box, dict)
        self.assertIsNotNone(box.get('resultSets', None))
        box = self.nbs.boxscore_usage('0021500001')
        self.assertIsInstance(box, dict)
        self.assertIsNotNone(box.get('resultSets', None))

    def test_playerstats(self):
        ps = self.nbs.playerstats('2016-17')
        self.assertIsInstance(ps, dict)
        rs = ps.get('resultSets', None)
        self.assertIsNotNone(rs)
        self.assertIsNotNone(rs[0].get('headers', None))

    def test_player_info(self):
        pinfo = self.nbs.player_info('203083', '2016-17')
        self.assertIsInstance(pinfo, dict)
        rs = pinfo.get('resultSets', None)
        self.assertIsNotNone(rs)
        self.assertIsNotNone(rs[0].get('headers', None))

    def test_one_player_gamelogs(self):
        pgl = self.nbs.one_player_gamelogs('203083', '2016-17')
        self.assertIsInstance(pgl, dict)
        rs = pgl.get('resultSets', None)
        self.assertIsNotNone(rs)
        self.assertIsNotNone(rs[0].get('headers', None))

    def test_players (self):
        players = self.nbs.players(season='2016-17', cs_only='1')
        self.assertIsInstance(players, dict)
        rs = players.get('resultSets', None)
        self.assertIsNotNone(rs)
        self.assertIsNotNone(rs[0].get('headers', None))

    def test_season_gamelogs(self):
        pgl = self.nbs.season_gamelogs(season='2016-17', player_or_team='P')
        self.assertIsInstance(pgl, dict)
        rs = pgl.get('resultSets', None)
        self.assertIsNotNone(rs)
        self.assertIsNotNone(rs[0].get('headers', None))
        tgl = self.nbs.season_gamelogs(season='2016-17', player_or_team='T')
        self.assertIsInstance(tgl, dict)
        rs = tgl.get('resultSets', None)
        self.assertIsNotNone(rs)
        self.assertIsNotNone(rs[0].get('headers', None))

    def test_team_dashboard(self):
        team_id = '1610612765'
        season = '2016-17'
        tdb = self.nbs.team_dashboard(team_id, season)
        self.assertIsInstance(tdb, dict)
        rs = tdb.get('resultSets', None)
        self.assertIsNotNone(rs)
        self.assertIsNotNone(rs[0].get('headers', None))

    def test_team_opponent_dashboard(self):
        season = '2016-17'
        tdb = self.nbs.team_opponent_dashboard(season)
        self.assertIsInstance(tdb, dict)
        rs = tdb.get('resultSets', None)
        self.assertIsNotNone(rs)
        self.assertIsNotNone(rs[0].get('headers', None))

    def test_one_team_gamelogs(self):
        team_id = '1610612765'
        season = '2016-17'
        tdb = self.nbs.one_team_gamelogs(team_id, season)
        self.assertIsInstance(tdb, dict)
        rs = tdb.get('resultSets', None)
        self.assertIsNotNone(rs)
        self.assertIsNotNone(rs[0].get('headers', None))

    def test_teamstats(self):
        season = '2016-17'
        ts = self.nbs.team_opponent_dashboard(season)
        self.assertIsInstance(ts, dict)
        rs = ts.get('resultSets', None)
        self.assertIsNotNone(rs)
        self.assertIsNotNone(rs[0].get('headers', None))

    def test_teams(self):
        t = self.nbs.teams()
        self.assertIsInstance(t, basestring)
        self.assertRegexpMatches(t, r'Pistons')

if __name__=='__main__':
    logging.basicConfig(level=logging.ERROR)
    unittest.main()
