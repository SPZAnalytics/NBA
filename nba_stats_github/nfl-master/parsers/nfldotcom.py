# json module in standard library could not parse

import demjson
import logging
import os
import pprint


class NFLDotComParser:
    '''
    Used to parse NFL.com GameCenter pages, which are json documents with game and play-by-play stats
    '''

    def __init__(self,**kwargs):

        logging.getLogger(__name__).addHandler(logging.NullHandler())

        if 'categories' in kwargs:
            self.categories = kwargs['categories']
        else:
            self.categories = ['passing', 'rushing', 'receiving', 'fumbles', 'kickret', 'puntret', 'defense']

    def _gamecenter_team(self, team):
        '''
        Parses home or away team into stats dictionary
        :param team(dict): dictionary representing home or away team
        :return players(dict): dictionary of stats for home or away team
        '''
        players = {}
        
        try:

            for category in self.categories:
                for player_id, player_stats in team[category].items():

                    if not player_id in players:
                        players[player_id] = {'player_id': player_id}

                    players[player_id][category] = player_stats

        except Exception:
            logging.exception('_gamecenter_team')

        return players

    def _merge_dicts(self, d1, d2):
        '''
        Cominbes home and away stats into one dictionary
        :param d1(dict):
        :param d2(dict):
        :return z(dict):
        '''
        z = d1.copy()
        z.update(d2)
        return z

    def gamecenter(self,gamecenter=None,fname=None):
        '''
        Parses gamecenter (json document) given a game_id and either a string or filename
        :param gamecenter(str):
        :param fname(str):
        :return: combined(dict): stats for home and away team
        '''

        # can pass string or filename
        if gamecenter:
            try:
                parsed = demjson.decode(gamecenter)
            except:
                logging.exception('json parse from content failed')

        elif fname:
            try:
                parsed = demjson.decode_file(fname)
            except:
                logging.exception('json parse from filename failed')

        else:
            raise ValueError('must pass content or filename')

        if parsed:
            game_id = parsed.keys()[0]
            home_team_stats = self._gamecenter_team(parsed[game_id]['home']['stats'])
            away_team_stats = self._gamecenter_team(parsed[game_id]['away']['stats'])

            # use player_id as a key, value is entire player dictionary (with player_id as duplicate)
            combined = self._merge_dicts(home_team_stats, away_team_stats)

        else:
            raise ValueError('parsed should not be null')

        '''
        puntret: avg, lng, lngtd, name, ret, tds
        fumbles: lost, name, rcv, tot, trcv, yds
        defense: ast, ffum, int, name, sk, tkl
        rushing: att, lng.lngtd, name, tds, twopta, twoptm, yds
        receiving: lng, lngtd, name, rec, tds, twopta, twoptm, yds
        passing: att, cmp, ints, name, tds, twopta, twoptm, yds
        '''

        return combined
        
if __name__ == "__main__":
    p = NFLComParser()
    fname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nfldotcom-sample.json')
    players = p.gamecenter(fname=fname)
    pprint.pprint(players)
