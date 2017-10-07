'''
games.py
gets list of games by season
can find game id for game_date and two teams

'''

import logging

from nfl.db import nflpg


class NFLGame(object):
    '''
    Usage:
        logging.basicConfig(level=logging.DEBUG)
        ng = NFLGame(db='nfl', user=USER, password=PWD)
        logging.debug(ng._gamedict.keys())
        logging.debug(len(ng.all_games()))
        logging.debug(ng.match_one_game(2015, 'CHI', 'GB'))
        logging.debug(ng.season_games(2015)[0:3])
        logging.debug(ng.team_season_games('CHI', 2015))
    '''

    def __init__(self, user=None, password=None, db=None, load_games=True):
        self._games = []
        self._gamedict = {}
        if load_games:
            if db and user and password:
                self.nflp = nflpg.NFLPostgres(user, password, db)
                self._load_games()
            else:
                logging.exception('need to pass database, user, and password to load games')

    def _game_date(self, gd):
        '''
        Adds game_date to game dictionary

        Args:
            gd: should be 10-digit int or str

        Returns:
            g(dict): game dict
        '''
        gd = str(gd)
        return '-'.join([gd[:4], gd[4:6], gd[6:8]])

    def _gdkey(self, g):
        '''

        Args:
            g(dict): game dictionary with minimum keys of season_year, away_team, home_team

        Returns:
            gdkey(str): e.g. 20160911_CHI_HOU
        '''
        return '{}_{}_{}'.format(g['season_year'], g['away_team'], g['home_team'])

    def _load_games(self):
        '''
        Does sql query and then loads list and gamedict for use by other methods
        '''
        sql = '''SELECT gsis_id, gamekey, season_year, week, home_team, away_team FROM game WHERE season_type = 'Regular';'''
        games = self.nflp.select_dict(sql)
        if games:
            self._games = games
            self._gamedict = {self._gdkey(g):g for g in games}

    def all_games(self):
        '''
        All games (since 2009 at least)
        Returns:
            games(list): of game dict
        '''
        if not self._games:
            self._load_games()
        return self._games

    def match_one_game(self, season, away_team, home_team):
        '''

        Args:
            game_datestr (str):
            away_team (str):
            home_team (str):

        Returns:
            gsis_id (str)
        '''
        if not self._games:
            self._load_games()
        g = {'season_year': season, 'away_team': away_team, 'home_team': home_team}
        logging.debug(g)
        logging.debug(self._gdkey(g))
        return self._gamedict.get(self._gdkey(g), None)

    def match_games(self, season=None, away_team=None, home_team=None):
        '''
        TODO: make this flexible based on season and teams

        Args:
            game_datestr (str):
            away_team (str):
            home_team (str):

        Returns:
            gsis_ids (list): of game dict
        '''
        if not self._games:
            self._load_games()

        return [g for g in self._games if g['season_year'] == season and g['home_team'] == home_team and g['away_team'] == away_team]

    def season_games(self, season):
        '''

        Args:
            season(int):

        Returns:
            games(list): of game dict
        '''
        if not self._games:
            self._load_games()
        return [g for g in self._games if g['season_year'] == season]

    def team_season_games(self, team, season):
        '''

        Args:
            team(str): use code like CHI, DET, etc.
            season(int): 2016, 2015, etc.

        Returns:
            games(list): of game dict
        '''
        if not self._games:
            self._load_games()
        return [v for k,v in self._gamedict.items() if team in k and str(season) in k]

if __name__ == '__main__':
    pass
