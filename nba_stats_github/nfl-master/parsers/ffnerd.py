# -*- coding: utf-8 -*-

import json
import logging


class FFNerdNFLParser(object):

    def __init__(self,**kwargs):

        if 'logger' in kwargs:
          self.logger = kwargs['logger']
        else:
          self.logger = logging.getLogger(__name__)

        if 'overall_rank_max' in kwargs:
          self.overall_rank_max = kwargs['overall_rank_max']
        else:
          self.overall_rank_max = 500

    def fix_header(self, header):
        '''
        Looks at global list of headers, can provide extras locally
        :param headers:
        :return:
        '''

        fixed = {
            'playerId': 'ffnerd_id',
            'fantasyPoints': 'fantasy_points',
            'nerdRank': 'ffnerd_rank',
        }

        # return fixed.get(header, header)
        #fixed_header = self._fix_header(header)

        # fixed_header none if not found, so use local list
        #if not fixed_header:
        
        return fixed.get(header, header)

        #else:
        #    return fixed_header

    def fix_headers(self, headers):
        '''
        Fixes all headers that are passed in headers parameter
        :param headers (list): the headers to fix - standardize on lowercase, full_name, etc.
        :return headers (list): the fixed headers
        '''
        return [self.fix_header(header) for header in headers]

    def _parse_projections(self, projections):
        '''
        Loops through projections, which are by position on ffnerd site, and processes into dictionary of player dictionaries
        :param projections (dict): key is position, value is json dictionary of player projections
        :return player_projecitons (dict): key is ffnerd_id, value is player dictionary
        '''

        player_projections = {}

        # {'QB': '{"DraftProjections":[{"playerId":"1932",
        # position is QB, position_json is the rest
        for position, position_json in projections.items():

            # the value is itself a json dictionary, so load json and get value of key DraftProjections
            for player in json.loads(position_json)['DraftProjections']:

                # returning a dictionary of dictionaries, key is the playerId (which fix_header changes to ffnerd_id)
                id = player['playerId']
                fixed_player = {}

                # fix the header(here, key) and use it to create new dictionary (fixed_player)
                for key, value in player.items():
                    fixed_player[self.fix_header(key)] = value

                # add item to dictionary of dictionaries
                player_projections[id] = fixed_player

        return player_projections

    def _parse_rankings(self, rankings):
        '''
        Takes rankings (list of player dictionaries) and processes into dictionary with key of ffnerd_id and value of player dictionary
        :param rankings (list): list of dictionaries of player rank
        :return player_rankings (dict): key is ffnerd_id, value is player dictionary
        '''

        player_rankings = {}

        # ['{"PPR":0,"DraftRankings":[{"playerId":"259","position":"RB","displayName":"Adrian Peterson",
        # DraftRankings has wanted data
        for player in json.loads(rankings[0])['DraftRankings']:

            # returning a dictionary of dictionaries, key is the playerId (which fix_header changes to ffnerd_id)
            id = player['playerId']
            fixed_player = {}

            # loop through dictionary, fix headers (here, keys) one at a time, populate fixed_player
            for key, value in player.items():
                fixed_player[self.fix_header(key)] = value

            # key is ffnerd_id, value is player dictionary
            player_rankings[id] = fixed_player

        return player_rankings

    def _parse_weekly_projections(self, projections):
        '''
        Loops through projections, which are by position on ffnerd site, and processes into dictionary of player dictionaries
        :param projections (dict): key is position, value is json dictionary of player projections
        :return player_projecitons (dict): key is ffnerd_id, value is player dictionary
        '''

        player_projections = {}

        for pos in ['QB', 'WR', 'RB', 'TE', 'DEF']:
            for player in json.loads(projections.get(pos)).get('Projections'):

                # returning a dictionary of dictionaries, key is the playerId (which fix_header changes to ffnerd_id)
                id = player['playerId']
                fixed_player = {}

                # fix the header(here, key) and use it to create new dictionary (fixed_player)
                for key, value in player.items():
                    fixed_player[self.fix_header(key)] = value

                # add item to dictionary of dictionaries
                player_projections[id] = fixed_player

        return player_projections

    def _parse_weekly_rankings(self, rankings):
        '''
        Takes rankings (list of player dictionaries) and processes into dictionary with key of ffnerd_id and value of player dictionary
        :param rankings (list): list of dictionaries of player rank
        :return player_rankings (dict): key is ffnerd_id, value is player dictionary
        '''

        player_rankings = {}

        for pos in ['QB', 'WR', 'RB', 'TE', 'DEF']:
            for player in json.loads(rankings.get(pos)).get('Rankings'):

                # returning a dictionary of dictionaries, key is the playerId (which fix_header changes to ffnerd_id)
                id = player['playerId']
                fixed_player = {}

                # loop through dictionary, fix headers (here, keys) one at a time, populate fixed_player
                for key, value in player.items():
                    fixed_player[self.fix_header(key)] = value

                # key is ffnerd_id, value is player dictionary
                player_rankings[id] = fixed_player

        return player_rankings

    def season_projections (self, projections, rankings):
        '''
        Takes projections and rankings, combines them, creates list of player dictionaries
        :param projections(dictionary): key is position (QB, etc.) and value is list of player dictionaries with projected stats
        :param rankings(list): list of player dictionaries with draft rankings
        :return players(list): list of player dictionaries
        '''

        players = []

        # want to create dictionary with player_id as key, value as dictionary
        player_rankings = self._parse_rankings(rankings)
        player_projections = self._parse_projections(projections)

        # merge the two dictionaries together, failed with many approaches
        # even if this is verbose it works, esp. for players who have rankings but no projections
        for id, player in player_rankings.items():

            # filter out scrubs and unwanted positions
            if player.get('position') not in ['QB', 'WR', 'RB', 'TE']:
                pass

            else:
                #first_last, full_name = NameMatcher.fix_name(player.get('full_name'))

                # stackoverflow code for merging 2 dictionaries
                x = player.copy()
                y = player_projections.get(id)

                if y is not None:
                    x.update(y)

                x['first_last'] = '%s %s' % (player.get('fname'), player.get('lname'))
                x['full_name'] = '%s, %s' % (player.get('lname'), player.get('fname'))

                players.append(x)

        return players

    def weekly_projections (self, projections, rankings):
        '''
        Takes projections and rankings, combines them, creates list of player dictionaries
        :param projections(dictionary): key is position (QB, etc.) and value is list of player dictionaries with projected stats
        :param rankings(list): list of player dictionaries with draft rankings
        :return players(list): list of player dictionaries
        '''

        players = []

        # want to create dictionary with player_id as key, value as dictionary
        player_rankings = self._parse_weekly_rankings(rankings)
        player_projections = self._parse_weekly_projections(projections)

        # merge the two dictionaries together, failed with many approaches
        # even if this is verbose it works, esp. for players who have rankings but no projections
        for id, player in player_rankings.items():

            # filter out scrubs and unwanted positions
            if player.get('position') not in ['QB', 'WR', 'RB', 'TE']:
                pass

            else:
                #first_last, full_name = NameMatcher.fix_name(player.get('full_name'))

                # stackoverflow code for merging 2 dictionaries
                x = player.copy()
                y = player_projections.get(id)

                if y is not None:
                    x.update(y)

                x['first_last'] = '%s %s' % (player.get('fname'), player.get('lname'))
                x['full_name'] = '%s, %s' % (player.get('lname'), player.get('fname'))

                players.append(x)

        return players

if __name__ == "__main__":
    pass
