import json
import logging
import os
import time

from nba.scrapers.nbacom import NBAComScraper
from nba.parsers.nbacom import NBAComParser


class NBAPlayers(object):
    '''
    TODO: need to update / merge this with the names module
    Provides for updating nba.com players table (stats.players)
    Also permits cross-reference of player names and player ids from various sites(stats.player_xref)

    Usage:
        np = NBAComPlayers(db=True)
        np.missing_players('2015-16')

    '''
    
    def __init__(self, db=None):
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        self._dk_players = []
        self.scraper = NBAComScraper()
        self.parser = NBAComParser()

        if db:
            self.nbadb = db

    def _convert_heigt(self, h):
        '''
        Converts height from 6-11 (feet-inches) to 73 (inches)
        Args:
            h(str): e.g. 6-7, 5-11, 7-1

        Returns:
            height(int): e.g. 79, 71, 85
        '''
        try:
            f, i = h.split('-')
            return int(f) * 12 + int(i)
        except:
            return None

    @property
    def dk_players(self):
        '''
        Dictionary of player_name: draftkings_player_id

        Returns:
            dk_players (dict): key is player name, value is dk_player_id
        '''
        if not self._dk_players:
            try:
                fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'dk_players.json')
                with open(fn, 'r') as infile:
                    self._dk_players = json.load(infile)
            except:
                logging.exception('could not open dk_players json file')

        return self._dk_players

    def missing_players(self, season):
        '''
        Looks for missing players by comparing current_season_gamelogs and players tables
        Fetches player_info by id, inserts player into players table

        Arguments:
            season (str): example '2015-16' for the current season

        Returns:
            missing (list): list of dictionaries that represent row in players table
        '''

        if not self.nbadb:
            raise ValueError('missing_players requires a database connection')

        missing = []

        # get list of ids that appear in current_season_gamelogs but not players
        sql = '''SELECT * FROM stats.players_to_add'''

        for pid in self.nbadb.select_list(sql):
            content = self.scraper.player_info(pid, season)
            pinfo = self.parser.player_info(content)

            pi = {k.lower(): v for k,v in pinfo.items()}
            pi.pop('games_played_flag', None)
            pi['nbacom_team_id'] = pi.get('team_id', None)
            pi.pop('team_id', None)
            pi['nbacom_position'] = pi.get('position', None)
            pi.pop('position', None)
            pi['nbacom_player_id'] = pi.get('person_id', None)
            pi.pop('person_id', None)

            if pi.get('height', None):
                pi['height'] = self._convert_heigt(pi['height'])

            # have to convert empty strings to None, otherwise insert fails for integer/numeric columns
            player_info= {}
            for k,v in pi.items():
                if not v:
                    player_info[k] = None
                else:
                    player_info[k] = v
            missing.append(player_info)

            if self.polite:
                time.sleep(1)

        if missing:
            self.nbadb.insert_dicts(missing, 'stats.players')

        return missing

    def player_xref(self, site_name):
        '''
        Obtains dictionary of site_player_id and nbacom_player_id

        Args:
            site_name (str): 'dk', 'fantasylabs', etc.
        Return:
            player_xref (dict): key is site_player_id
        '''

        sql = '''SELECT nbacom_player_id, site_player_id FROM stats.player_xref WHERE site='{0}' ORDER by nbacom_player_id'''
        xref = self.nbadb.select_dict(sql.format(site_name))
        return {p.get('site_player_id'): p.get('nbacom_player_id') for p in xref if p.get('site_player_id')}

    def site_to_nbacom(self, site, player_name):
        '''
        Returns dictionary with name of player on site, value is list of name and id of player on nba.com

        Arguments:
            site (str): 'dk', 'fd', 'rg', 'doug', 'espn'

        Returns:
            players (dict): key is player name on site, value is list [nbacom_player_name, nbacom_player id]
        '''

        if site.lower() not in self.sites:
            # should try name matcher
            pass

        elif site.lower() == 'dk':
            return self._dk_name(player_name)

        elif 'doug' in site.lower():
            return self._doug_name(player_name)

        elif 'espn' in site.lower():
            return self._espn_name(player_name)

        elif site.lower() == 'fd' or 'duel' in site.lower():
            return self._fd_name(player_name)

        elif site.lower() == 'fl' or 'labs' in site.lower():
            return self._fl_name(player_name)

        elif site.lower() == 'rg' or 'guru' in site.lower():
            return self._rg_name(player_name)

if __name__ == '__main__':
    pass
