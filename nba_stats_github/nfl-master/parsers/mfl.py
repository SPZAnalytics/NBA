# -*- coding: utf-8 -*-

import json
import logging
import pprint
import re
import xml.etree.ElementTree as ET

from NFLProjectionsParser import NFLProjectionsParser
import NameMatcher

class MyFantasyLeagueNFLParser(NFLProjectionsParser):
    '''
    Parses xml from myfantasyleague.com API
    
    Example:
        p = MyFantasyLeagueNFLParser()
        players = p.players(content)
    '''

    def __init__(self,**kwargs):
        '''
        Args:
            **kwargs: logger (logging.Logger)
        '''

        if 'logger' in kwargs:
          self.logger = kwargs['logger']
        else:
          self.logger = logging.getLogger(__name__)

    def _first_last(self, name):
        (last, first) = [x.strip() for x in name.split(',')]
        return '%s %s' % (first, last)

    def fix_header(self, header):
        '''
        Looks at global list of headers, can provide extras locally
        :param headers:
        :return:
        '''

        fixed = {
            'id': 'ffcalculator_id',
            'rk': 'overall_rank',
            'avg': 'fantasy_points_per_game',
        }

        #return fixed.get(header, header)
        fixed_header = self._fix_header(header)

        # fixed_header none if not found, so use local list
        if not fixed_header:
            return fixed.get(header, header)

        else:
            return fixed_header

    def fix_headers(self, headers):
        '''

        :param headers:
        :return:
        '''
        return [self.fix_header(header) for header in headers]

    def players (self, positions, content=None, fname=None):
        '''
        Parses xml and returns list of player dictionaries
        Args:
            content (str): xml typically fetched by Scraper class
        Returns:
            List of dictionaries if successful, empty list otherwise.
        '''

        players = []

        if content:
            root = ET.fromstring(content)
        elif fname:
            root = ET.parse(fname).getroot()
            logging.debug(root)
        else:
            raise ValueError('must pass content or filename')

        for item in root.iter('player'):
            logging.debug(item)
            attributes = item.attrib
            position = attributes.get('position', None)

            # don't want defensive players, for example, can also exclude punters/kickers
            if not position or position not in positions:
                logging.debug('not position or position not in positions')

            else:
                player = {}

                for k, v in attributes.items():
                    player[self.fix_header(k)] = v

                player['first_last'] = self._first_last(player['full_name'])
                players.append(player)

        return players

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    p = MyFantasyLeagueNFLParser()

    '''
    fname = 'players.xml'
    outfname = 'players.json'
    positions = ['QB', 'RB', 'WR', 'TE']
    players = p.players(positions=positions, fname=fname)

    with open(outfname, 'w') as outfile:
        json.dump(players, outfile, indent=4, sort_keys=True)
    '''