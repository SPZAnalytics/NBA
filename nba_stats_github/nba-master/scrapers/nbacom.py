from __future__ import print_function

from collections import defaultdict
import logging
import os

from nba.scrapers.scraper import BasketballScraper


class NBAComScraper(BasketballScraper):
    '''
    '''

    def __init__(self, headers=None, cookies=None, cache_name=None, expire_hours=12, as_string=False):
        '''
        Scraper for stats.nba.com (informal) API

        Args:
            headers: dictionary of HTTP headers
            cookies: cookie object, such as browsercookie.firefox()
            cache_name: str 'nbacomscraper'
            expire_hours: how long to cache requests
            as_string: return as raw string rather than json parsed into python data structure
        '''
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        BasketballScraper.__init__(self, headers=headers, cookies=cookies,
                                   cache_name=cache_name, expire_hours=expire_hours, as_string=as_string)

    def boxscore_traditional(self, game_id):
        '''
        Boxscore from a single game

        Arguments:
            game_id: numeric identifier of game

        Returns:
            content: python data structure of json documnt
        '''
        base_url = 'http://stats.nba.com/stats/boxscoretraditionalv2?'
        params = {
          'EndPeriod': '10',
          'EndRange': '100000',
          'GameID': game_id,
          'RangeType': '2',
          'SeasonType': 'Regular Season',
          'StartPeriod': '1',
          'StartRange': '0'
        }

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content


    def boxscore_advanced(self, game_id):
        '''
        Boxscore from a single game

        Arguments:
            game_id: numeric identifier of game (has to be 10-digit, may need two leading zeroes)
        Returns:
            content: python data structure of json document
        '''
        base_url = 'http://stats.nba.com/stats/boxscoreadvancedv2?'
        if len(str(game_id)) == 8:
            game_id = '00' + str(game_id)
        params = {
            'GameID': game_id,
            'StartPeriod': 1,
            'EndPeriod': 10,
            'StartRange': 0,
            'EndRange': 28800,
            'RangeType': 0
        }

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def boxscore_misc(self, game_id):
        '''
        Boxscore from a single game

        Arguments:
            game_id: numeric identifier of game (has to be 10-digit, may need two leading zeroes)

        Returns:
            content: python data structure of json document
        '''
        base_url = 'http://stats.nba.com/stats/boxscoremiscv2?'
        if len(str(game_id)) == 8:
            game_id = '00' + str(game_id)
        params = {
            'GameID': game_id,
            'StartPeriod': 1,
            'EndPeriod': 10,
            'StartRange': 0,
            'EndRange': 28800,
            'RangeType': 0
        }

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def boxscore_scoring(self, game_id):
        '''
        Boxscore from a single game

        Arguments:
            game_id: numeric identifier of game (has to be 10-digit, may need two leading zeroes)

        Returns:
            content: python data structure of json document
        '''
        base_url = 'http://stats.nba.com/stats/boxscorescoringv2?'
        if len(str(game_id)) == 8:
            game_id = '00' + str(game_id)
        params = {
            'GameID': game_id,
            'StartPeriod': 1,
            'EndPeriod': 10,
            'StartRange': 0,
            'EndRange': 28800,
            'RangeType': 0
        }

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def boxscore_usage(self, game_id):
        '''
        Boxscore from a single game

        Arguments:
            game_id: numeric identifier of game (has to be 10-digit, may need two leading zeroes)

        Returns:
            content: python data structure of json document
        '''
        base_url = 'http://stats.nba.com/stats/boxscoreusagev2?'
        if len(str(game_id)) == 8:
            game_id = '00' + str(game_id)

        params = {
            'GameID': game_id,
            'StartPeriod': 1,
            'EndPeriod': 10,
            'StartRange': 0,
            'EndRange': 28800,
            'RangeType': 0
        }

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def combined_boxscore(self, gid):
        '''
        Download boxscores for all of the game_ids provided

        Arguments:
            gid(list): nba.com game_id

        Returns:
            boxes(dict): keys are the type of boxscore, value is parsed json
        '''
        # traditional, advanced, misc, scoring, usage
        boxes = defaultdict(dict)

        # transform to string with leading zeroes
        if len(gid) == 8:
            gid = '00{0}'.format(gid)
        boxes['traditional'] = self.boxscore_traditional(gid)
        boxes['advanced'] = self.boxscore_advanced(gid)
        boxes['misc'] = self.boxscore_misc(gid)
        boxes['scoring'] = self.boxscore_scoring(gid)
        boxes['usage'] = self.boxscore_usage(gid)
        return boxes

    def games(self, season_year):
        '''
        All of the games in an nba season. Part of v2015 API, does not work before 2015 season.

        Args:
            season_year(int): the 2016-17 season would be 2016

        Returns:
            Parsed json into dict
        '''
        url = 'http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{}/league/00_full_schedule.json'
        content = self.get_json(url=url.format(season_year))
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def league_schedule(self, season_year):
        '''
        All of the games in an nba season. Part of v2015 API, does not work before 2015 season.

        Args:
            season_year(int): the 2016-17 season would be 2016

        Returns:
            Parsed json into dict
        '''
        url = 'http://data.nba.com/data/10s/prod/v1/{}/schedule.json'
        content = self.get_json(url=url.format(season_year))
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def one_player_gamelogs(self, player_id, season):
        '''
        All of the gamelogs for one player in a single season

        Args:
            player_id: int
            season: str e.g. 2016-17

        Returns:
            Parsed json as dict
        '''
        base_url = 'http://stats.nba.com/stats/playergamelog?'
        params = {
          'LeagueID': '00',
          'PlayerID': player_id,
          'Season': season,
          'SeasonType': 'Regular Season'
        }

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def one_team_gamelogs(self, team_id, season):
        '''
        All of the gamelogs for one team in a single season

        Args:
            team_id: int
            season: str e.g. 2016-17

        Returns:
            Parsed json as dict
        '''
        base_url = 'http://stats.nba.com/stats/teamgamelog?'
        params = {
          'LeagueID': '00',
          'TeamID': team_id,
          'Season': season,
          'SeasonType': 'Regular Season'
        }

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def player_info(self, player_id, season):
        '''
        Gets details about player, such as height, weight, college, draft slot

        Args:
            player_id: int nbacom_player_id
            season: str e.g. 2015-16

        Returns:
            playerinfo dict
        '''
        base_url = 'http://stats.nba.com/stats/commonplayerinfo?'
        params = {
          'LeagueID': '00',
          'PlayerID': player_id,
          'Season': season,
          'SeasonType': 'Regular Season'
        }

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def players(self, season, cs_only=0):
        '''
        Gets players, either all of them or only those from the current season

        Args:
            season: str e.g. 2015-16
            cs_only: bool 1 or 0

        Returns:
            players: list of player dict
        '''
        base_url = 'http://stats.nba.com/stats/commonallplayers?'
        params = {
          'IsOnlyCurrentSeason': cs_only,
          'LeagueID': '00',
          'Season': season,
        }

        return self.get_json(base_url, payload=params)

    def players_v2015(self, season_year):
        '''
        All active players. Part of v2015 API, does not work before 2015 season.

        Args:
            season_year(int): the 2016-17 season would be 2016

        Returns:
            Parsed json into dict
        '''
        url = 'http://data.nba.com/data/10s/prod/v1/{}/players.json'
        content = self.get_json(url=url.format(season_year))
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def playerstats(self, season, **kwargs):
        '''
        Document has one line of stats per player

        Arguments:
            season(str): such as 2015-16

        Returns:
            content: parsed json response from nba.com
        '''
        base_url = 'http://stats.nba.com/stats/leaguedashplayerstats?'

        # measure_type allows you to choose between Base and Advanced
        # per_mode can be Totals or PerGame
        # date_from and date_to allow you to select a specific day or a range of days
        # last_n_games allows picking 3, 5, 10, etc. game window='2014-15',per_mode='Totals',season_type='Regular Season',date_from='',date_to='',measure_type='Base',
        # last_n_games=0,month=0,opponent_team_id=0
        params = {
          'DateFrom': '',
          'DateTo': '',
          'GameScope': '',
          'GameSegment': '',
          'LastNGames': '0',
          'LeagueID': '00',
          'Location': '',
          'MeasureType': 'Base',
          'Month': '0',
          'OpponentTeamID': '0',
          'Outcome': '',
          'PaceAdjust': 'N',
          'PerMode': 'Totals',
          'Period': '0',
          'PlayerExperience': '',
          'PlayerPosition': '',
          'PlusMinus': 'N',
          'Rank': 'N',
          'Season': season,
          'SeasonSegment': '',
          'SeasonType': 'Regular Season',
          'StarterBench': '',
          'VsConference': '',
          'VsDivision': ''
        }

        # override defaults with **kwargs
        for key, value in kwargs.items():
            if key in params:
                params[key] = value

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        return content

    def scoreboard(self, game_date):
        '''
        Scoreboard for single game_date

        Args:
            game_date: str YYYY-mm-dd format

        Returns:
            parsed json
        '''
        base_url = 'http://stats.nba.com/stats/scoreboardV2?'
        params = {
          'DayOffset': '0',
          'LeagueID': '00',
          'GameDate': game_date,
        }

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def season_gamelogs(self, season, player_or_team, **kwargs):
        '''
        Team or player gamelogs for entire season

        Args:
            season: str e.g. 2015-16
            player_or_team: 'P' or 'T'

        Returns:
            content: json parsed into dict
        '''
        base_url = 'http://stats.nba.com/stats/leaguegamelog?'
        params = {
          'Counter': '0',
          'Direction': 'DESC',
          'LeagueID': '00',
          'PlayerOrTeam': player_or_team,
          'Season': season,
          'SeasonType': 'Regular Season',
          'Sorter': 'PTS'
        }

        # override defaults with **kwargs
        for key, value in kwargs.items():
            if key in params:
                params[key] = value

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def team_dashboard(self, team_id, season, **kwargs):
        '''
        Stats for single team in single season

        Args:
            team_id: int
            season: str e.g. '2016-17'
            **kwargs:

        Returns:
            dict of team statistics
        '''
        # measure_type allows you to choose between Base and Advanced
        # per_mode can be Totals or PerGame
        # date_from and date_to allow you to select a specific day or a range of days
        # last_n_games allows picking 3, 5, 10, etc. game window
        base_url = 'http://stats.nba.com/stats/teamdashboardbygeneralsplits?'
        params = {
          'DateFrom': '',
          'DateTo': '',
          'GameSegment': '',
          'LastNGames': '0',
          'LeagueID': '00',
          'Location': '',
          'MeasureType': 'Base',
          'Month': '0',
          'OpponentTeamID': '0',
          'Outcome': '',
          'PORound': '0',
          'PaceAdjust': 'N',
          'PerMode': 'PerGame',
          'Period': '0',
          'PlusMinus': 'N',
          'Rank': 'N',
          'Season': season,
          'SeasonSegment': '',
          'SeasonType': 'Regular Season',
          'ShotClockRange': '',
          'TeamID': team_id,
          'VsConference': '',
          'VsDivision': ''
        }

        # override defaults with **kwargs
        for key, value in kwargs.items():
            if key in params:
                params[key] = value

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def team_opponent_dashboard(self, season, **kwargs):
        '''
        Returns team_opponent stats for every team in league

        Args:
            season: str e.g. '2016-17'
            **kwargs:

        Returns:
            dict of team opponent statistics
        '''
        base_url = 'http://stats.nba.com/stats/leaguedashteamstats?'
        params = {
          'DateFrom': '',
          'DateTo': '',
          'GameSegment': '',
          'LastNGames': '0',
          'LeagueID': '00',
          'Location': '',
          'MeasureType': 'Opponent',
          'Month': '0',
          'OpponentTeamID': '0',
          'Outcome': '',
          'PORound': '0',
          'PaceAdjust': 'N',
          'PerMode': 'PerGame',
          'Period': '0',
          'PlusMinus': 'N',
          'Rank': 'N',
          'Season': season,
          'SeasonSegment': '',
          'SeasonType': 'Regular Season',
          'ShotClockRange': '',
          'TeamID': '0',
          'VsConference': '',
          'VsDivision': ''
        }

        # override defaults with **kwargs
        for key, value in kwargs.items():
            if key in params:
                params[key] = value

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def teams(self):
        '''
        Gets javascript file with js variable containing team_ids and team names

        Returns:
            content is javascript code
        '''
        #  nba.com stores team_id and team_code as a variable in a javascript file
        url = 'http://stats.nba.com/scripts/custom.min.js'
        content = self.get(url)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        return content

    def teams_v2015(self, season_year):
        '''
        Gets team information - v2015 API

        Args:
            season_year: int such as 2016 for 2016-17 season

        Returns:
            dict
        '''
        base_url = 'http://data.nba.com/data/10s/prod/v1/{}/teams.json'
        content = self.get_json(base_url.format(season_year))
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

    def teamstats(self, season, **kwargs):
        '''
        Stats for every team in single season

        Args:
            season: str e.g. '2016-17'
            **kwargs:

        Returns:
            dict of team statistics
        '''
        # measure_type allows you to choose between Base and Advanced
        # per_mode can be Totals or PerGame
        # date_from and date_to allow you to select a specific day or a range of days
        # last_n_games allows picking 3, 5, 10, etc. game window
        base_url = 'http://stats.nba.com/stats/leaguedashteamstats?'

        params = {
          'DateFrom': '',
          'DateTo': '',
          'GameScope': '',
          'GameSegment': '',
          'LastNGames': '0',
          'LeagueID': '00',
          'Location': '',
          'MeasureType': 'Base',
          'Month': '0',
          'OpponentTeamID': '0',
          'Outcome': '',
          'PaceAdjust': 'N',
          'PerMode': 'PerGame',
          'Period': '0',
          'PlayerExperience': '',
          'PlayerPosition': '',
          'PlusMinus': 'N',
          'Rank': 'N',
          'Season': season,
          'SeasonSegment': '',
          'SeasonType': 'Regular Season',
          'ShotClockRange': '',
          'StarterBench': '',
          'TeamID': '0',
          'VsConference': '',
          'VsDivision': ''
        }

        # override defaults with **kwargs
        for key, value in kwargs.items():
            if key in params:
                params[key] = value

        content = self.get_json(base_url, payload=params)
        if not content:
            logging.error('could not get {}'.format(self.urls[-1]))
        else:
            logging.debug('got {}'.format(self.urls[-1]))
        return content

if __name__ == "__main__":
    pass