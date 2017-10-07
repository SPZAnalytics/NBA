from __future__ import absolute_import

import logging
import os
import unittest

from nba.parsers.nbacom import NBAComParser
from nba.scrapers.nbacom import NBAComScraper


class NBAComParser_test(unittest.TestCase):

    def setUp(self):
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        self.nbs = NBAComScraper()
        self.nbp = NBAComParser()

    def _get_from_file(self, fn):
        if os.path.isfile(fn):
            try:
                with open(fn) as x:
                    return x.read()
            except:
                logging.exception('could not read from file ' + fn)
        return None

    def _one_player_gamelogs(self,fn='one_player_gamelogs.json'):
        return self._get_from_file(fn)

    def _one_team_gamelogs(self,fn='one_team_gamelogs.json'):
        return self._get_from_file(fn)

    def _player_boxscore_traditional(self,fn='boxscore_traditional.json'):
        return self._get_from_file(fn)

    def _player_gamelogs(self,fn='player_gamelogs.json'):
        return self._get_from_file(fn)

    def _player_info(self,fn='player_info.json'):
        return self._get_from_file(fn)

    def _players(self,fn='players.json'):
        return self._get_from_file(fn)

    def _playerstats(self,fn='player_stats.json'):
        return self._get_from_file(fn)

    def _scoreboard(self,fn='scoreboard.json'):
        return self._get_from_file(fn)

    def _team_dashboard(self,fn='team_dashboard.json'):
        return self._get_from_file(fn)

    def _team_gamelogs(self,fn='team_game_logs.json'):
        return self._get_from_file(fn)

    def _team_opponent_dashboard(self,fn='team_opponent_dashboard.json'):
        return self._get_from_file(fn)

    def _teams(self,fn='teams.js'):
        return self._get_from_file(fn)

    def _teamstats(self,fn='teamstats.json'):
        return self._get_from_file(fn)

    def test_boxscore(self):
        content = self._player_boxscore_traditional()
        if not content:
            content = self.nbs.boxscore_traditional('0021500001')
        players, teams, starter_bench = self.nbp.boxscore_traditional(content)
        self.assertIsInstance(players, list)
        self.assertIsInstance(teams, list)
        self.assertIsInstance(players[0], dict)
        self.assertIn('MIN_PLAYED', players[0], "players should have min_played")
        self.assertIn('MIN_PLAYED', players[8], "players should have min_played")
        self.assertIn('MIN', teams[0], "teams should have min")
        self.assertIn('MIN', teams[1], "teams should have min")

    def test_one_player_gamelogs(self):
        content = self._one_player_gamelogs()
        if not content:
            content = self.nbs.one_player_gamelogs('203083', '2015-16')
        gls = self.nbp.one_player_gamelogs(content)
        self.assertIsInstance(gls, list)
        self.assertIsInstance(gls[0], dict)
        logging.info(gls)

    def test_one_team_gamelogs(self):
        content = self._one_team_gamelogs()
        if not content:
            team_id = '1610612765'
            season = '2015-16'
            content = self.nbs.one_team_gamelogs(team_id, season)
        gls = self.nbp.one_team_gamelogs(content)
        self.assertIsInstance(gls, list)
        self.assertIsInstance(gls[0], dict)

    def test_player_info(self):
        content = self._player_info()
        if not content:
            content = self.nbs.player_info('201939', '2015-16')
        pinfo = self.nbp.player_info(content)
        self.assertIsInstance(pinfo, dict)

    def test_players(self):
        content = self._players()
        if not content:
            content = self.nbs.players(season='2016-17', cs_only='1')
        ps = self.nbp.players(content)
        self.assertIsInstance(ps, list)
        self.assertIsNotNone(ps[0], 'ps should not be none')

    def test_playerstats(self):
        content = self._playerstats()
        if not content:
            statdate = '2016-01-20'
            content = self.nbs.playerstats('2015-16')
            ps = self.nbp.playerstats(content, statdate)
        self.assertIsInstance(ps, list)
        self.assertEqual(ps[0].get('STATDATE'), statdate)

    def test_season_gamelogs(self):
        team_content = self._team_gamelogs()
        player_content = self._player_gamelogs()
        if not team_content:
            team_content = self.nbs.season_gamelogs('2015-16', 'T')
        if not player_content:
            player_content = self.nbs.season_gamelogs('2015-16', 'P')
        team_gl = self.nbp.season_gamelogs(team_content, 'T')
        player_gl = self.nbp.season_gamelogs(player_content, 'P')
        self.assertIsInstance(player_gl, list)
        self.assertIsInstance(team_gl, list)
        self.assertIn('GAME_ID', player_gl[0], "players should have game_id")
        self.assertIn('GAME_ID', team_gl[0], "teams should have game_id")

    def test_team_dashboard(self):
        content = self._team_dashboard()
        if not content:
            team_id = '1610612765'
            season = '2015-16'
            content = self.nbs.team_dashboard(team_id, season)
        td = self.nbp.team_dashboard(content)
        self.assertIsInstance(td, dict)
        self.assertIn('overall', td, "dashboard has overall")

    def test_team_opponent_dashboard(self):
        content = self._team_opponent_dashboard()
        if not content:
            season = '2015-16'
            content = self.nbs.team_opponent_dashboard(season)
        td = self.nbp.team_opponent_dashboard(content)
        self.assertIsInstance(td, list)
        self.assertIsNotNone(td[0], 'td should not be None')

    def test_teams(self):
        content = self._teams()
        if not content:
            content = self.nbs.teams()
        tms = self.nbp.teams(content)
        self.assertIsInstance(tms, dict)
        self.assertIsNotNone(tms, 'tms should not be None')

    def test_teamstats(self):
        content = self._teamstats()
        if not content:
            season = '2015-16'
            content = self.nbs.teamstats(season)
        ts = self.nbp.teamstats(content)
        self.assertIsInstance(ts, list)
        self.assertIsNotNone(ts[0], 'ts should not be None')

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()