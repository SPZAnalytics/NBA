from __future__ import print_function

import logging

from nba.db.pgsql import NBAPostgres
from nba.pipelines.nbacom import *

class NBAComPg(NBAPostgres):
    '''
    Usage:
        from nba.agents.nbacom import NBAComAgent
        from nba.db.nbacom import NBAComPg

        nbap = NBAComPg(username=un, password=pw, database=db)
        a = NBAComAgent()
        tgl = a.cs_team_gamelogs('2016-17')
        nbap.insert_team_gamelogs(tgl, season=2017, nbacom_season_id=22016, table_name)
    '''


    def __init__(self, username, password, database='nbadb', host='localhost', port=5432, table_names=None):
        '''
        TODO: add table_names as property
        '''
        NBAPostgres.__init__(self, username, password, database)
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        if table_names:
            self.table_names = table_names
        else:
            self.table_names = {'pgl': 'player_gamelogs', 'tgl': 'team_gamelogs',
                                'pl': 'players', 'ps': 'playerstats_daily', 'ts': 'teamstats_daily',
                                'tod': 'team_opponent_dashboard'}


    def missing_pgl(self):
        '''
        Queries nbadb for game_ids of current-season games that don't appear in player_gamelogs

        Returns:
            List of game_ids(int)
        '''
        q = """SELECT * FROM missing_playergl"""
        return self.select_list(q)


    def missing_tgl(self):
        '''
        Queries nbadb for game_ids of current-season games that don't appear in team_gamelogs

        Returns:
            List of game_ids(int)
        '''
        q = """SELECT * FROM missing_teamgl"""
        return self.select_list(q)


    def insert_games(self, games, table_name):
        '''

        Args:
            games(list): of dict
            table_name(str):

        Returns:
            status
        '''
        return self.insert_dicts(games, table_name)


    def insert_player_boxscores(self, player_boxscores, player_table_name):

        omit = ['COMMENT', 'FG3_PCT', 'FG_PCT', 'FT_PCT', 'TEAM_CITY', 'TEAM_NAME']
        cleaned_players = []

        for player in player_boxscores:
            clean_player = {k.lower(): v for k, v in player.iteritems() if k not in omit}
            if clean_player.has_key('to'):
                clean_player['tov'] = clean_player['to']
                clean_player.pop('to', None)
            clean_player.pop('team_abbreviation', None)
            cleaned_players.append(clean_player)

        if cleaned_players:
            self.insert_dicts(cleaned_players, player_table_name)
            return cleaned_players
        else:
            logging.error('no boxscores to insert')


    def insert_player_gamelogs(self, gl):
        '''
        Takes list of player gamelogs, reformats and inserts into player gamelogs table

        Args:
            players(list): of player dict
        '''
        toins = player_gamelogs_table(gl)
        if toins:
            self.insert_dicts(toins, self.table_names.get('pgl'))


    def insert_players(self, players):
        '''
        Takes list of players, reformats and inserts into players table

        Args:
            players(list): of player dict
        '''
        toins = players_table(players)
        if toins:
            self.insert_dicts(toins, self.table_names.get('pl'))


    def insert_playerstats(self, ps, as_of):
        '''
        Inserts base + advanced playerstats into table

        Arguments:
            playerstats(list): list of player dictionaries
        '''
        if ps:
            self.insert_dicts(playerstats_table(ps, as_of), self.table_names.get('ps'))


    def insert_team_gamelogs(self, tgl):
        '''
        Inserts merged list of team gamelogs base + advanced

        Arguments:
            tgl: list of team gamelogs
        '''
        toins = team_gamelogs_table(tgl)
        if toins:
            self.insert_dicts(toins, self.table_names.get('tgl'))


    def insert_team_opponent_dashboards(self, stats, as_of):
        '''
        Inserts dashboards

        Arguments:
            stats(list): list of dictionaries
            as_of(str): in YYYY-MM-DD format

        Returns:
            list of dict
        '''
        to_ins = team_opponent_dashboards_table(stats, as_of)
        if to_ins:
            self.insert_dicts(to_ins, self.table_names.get('tod'))


    def insert_teamstats(self, stats, as_of):
        '''
        Inserts base + advanced stats

        Arguments:

            stats(list): list of dictionaries
            as_of(str): in YYYY-MM-DD format

        Returns:
            list of dict
        '''
        to_ins = teamstats_table(stats, as_of)
        if to_ins:
            self.insert_dicts(to_ins, self.table_names.get('ts'))


    def update_players(self, players, table_name=None):
        '''
        Inserts new players into players table

        Args:
            players(list): of player dict
            table_name(str): full name of table, like stats.players

        Returns:
            None
        '''
        if not table_name:
            table_name = self.table_names.get('pl')
        self.insert_dicts(players, table_name)


    def update_positions(self, table_name=None):
        '''
        Updates gamelogs table with positions from players table
        '''
        if not table_name:
            table_name = self.table_name.get('pgl')
        sql = """UPDATE {0}
                SET position_group=subquery.position_group, primary_position=subquery.primary_position
                FROM (SELECT nbacom_player_id, position_group, primary_position FROM stats.players) AS subquery
                WHERE ({0}.position_group IS NULL OR {0}.primary_position IS NULL) AND {0}.nbacom_player_id=subquery.nbacom_player_id;
              """
        self.update(sql.format(table_name))


    def update_teamids(self, table_name=None):
        '''
        Updates gamelogs table with teamids
        '''
        if not table_name:
            table_name = self.table_name.get('pgl')
        sql = """UPDATE {0}
                SET team_id=subquery.team_id
                FROM (SELECT nbacom_team_id as team_id, team_code FROM stats.teams) AS subquery
                WHERE {0}.team_id IS NULL AND {0}.team_code=subquery.team_code;
              """
        self.update(sql.format(table_name))


if __name__ == '__main__':
    pass