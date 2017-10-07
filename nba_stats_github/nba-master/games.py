try:
    import pickle as pickle
except:
    import pickle

import csv
import json
import logging
import os

from nba.db import pgsql

class NBAGames():
    '''
    Provides lookup table for games. Can use "gamecode" format to figure out nbacom_game_id, visitor_team_id, home_team_id
    Can create from file or from database table

    Usage:
        g = NBAGames()
        games = g.games()
        gamecode = '20150101/CLECHI'
        game_ids = g.game_ids(gamecode)
    '''


    def __init__(self):

        logging.getLogger(__name__).addHandler(logging.NullHandler())
        self._games = {}


    def _games_from_db(self, table_name):
        '''
        Gets nba games from database table

        Arguments:
            table_name(str): database table with games data

        Returns:
            games(dict): key is gamecode, value is dict with keys nbacom_game_id, visitor_team_id, home_team_id
        '''

        if not self._pg:
            self._pg = postgres.NBAComPostrges()

        try:
            sql = """SELECT gamecode, game_id, visitor_team_id, home_team_id FROM games"""
            self._games = self._pg.select_dict(sql)

        except:
            logging.exception('could not get games from table {0}'.format(table_name))

        return self._games
        
    def _games_from_file(self, file_name):
        '''
        Gets nba games from file, such as pickle or json

        Arguments:
            file_name(str): file with games data

        Returns:
            games(dict): key is gamecode, value is dict with keys nbacom_game_id, visitor_team_id, home_team_id
        '''
        
        fname, fextension = os.path.splitext(file_name)

        if fextension == '.pkl':
            try:
                with open(file_name, 'rb') as infile:
                    self._games = pickle.load(infile)

            except:
                logging.exception('could not load games from pickle file')
        
        elif fextension == '.json':
            try:
                with open(file_name, 'r') as infile:
                    self._games = json.load(infile)

            except:
                logging.exception('could not load games from json file')

        return self._games

    def game_ids(self, gamecode):
        '''
        Provides lookup dictionary for game information based on gamecode ('20150101/CLECHI')

        Arguments:
            gamecode(str): in YYYYMMDD/VISHOM format

        Returns:
            game_ids(dict): keys are nbacom_game_id, visitor_team_id, home_team_id

        '''

        return self._games.get(gamecode, None)
       
    def games(self,file_name=None,table_name=None):
        '''
        Dictionary of gamecode: {nbacom_game_id, visitor_team_id, home_team_id}

        Arguments:
            file_name(str): file with games datastructure
            table_name(str): database table for games (typically 'games')

        Returns:
            games(dict): keys are gamecode, values are dict with keys nbacom_game_id, visitor_team_id, home_team_id

        '''

        if not self._games:
            if file_name:
                self._games = self._games_from_file(file_name)

            elif table_name:
                if not self._db:
                    self._db = postgres.NBAComPostrges()
                self._games = self._games_from_db(table_name)
            
        return self._games

if __name__ == '__main__':
    pass
