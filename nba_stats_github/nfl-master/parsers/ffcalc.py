# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import logging
import math
import pprint
import re
import xml.etree.ElementTree as ET

from NFLProjectionsParser import NFLProjectionsParser


class FantasyFootballCalculatorParser(NFLProjectionsParser):
    '''
    Parses html of NFL fantasy projections page of fantasycalculator.com into player dictionaries

    Example:
        p = FantasyFootballCalculatorParser()
        players = p.projections(content)
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

        if 'positions' in 'kwargs':
            self.positions = kwargs['positions']
        else:
            self.positions = ['QB', 'RB', 'WR', 'TE']

    def adp (self, content, my_league_size):
        '''
        Parses xml and returns list of player dictionaries
        Args:
            content (str): xml typically fetched by FantasyCalculatorNFLScraper class
        Returns:
            List of dictionaries if successful, empty list otherwise.
        '''

        players = []

        root = ET.fromstring(content)

        adp_league_size = int(root.find('.//teams').text)

        for item in root.findall('.//player'):

            if item.find('./pos').text.lower() == 'pk':
                pass

            else:
                player = {}

                for child in item.findall('*'):
                    if child.tag.lower() == 'adp':
                        fixed = self._fix_adp(child.text, adp_league_size, my_league_size)
                        player['overall_pick'] = fixed['overall_pick']
                        player['round'] = int(fixed['round'])
                        player['pick'] = int(fixed['pick'])

                    else:
                        player[self.fix_header(child.tag.lower())] = child.text

                players.append(player)

        return players

    def _fix_adp(self, adp, adp_league_size, my_league_size):
        '''
        Data is in R.PP format, so you have to translate those numbers to an overall pick
        and R.PP format for the size of your league
        :param adp(str): is in round.pick format
        :param adp_league_size(int): number of teams in types of draft (8, 10, 12, 14)
        :return: Dictionary: is overall, round, pick based on your league size
        '''
        round, pick = adp.split('.')
        overall_pick = ((int(round) - 1) * adp_league_size) + int(pick)

        adjusted_round = math.ceil(overall_pick/float(my_league_size))

        if adjusted_round == 1:
            adjusted_pick = overall_pick
        else:
            adjusted_pick = overall_pick - ((adjusted_round - 1) * my_league_size)

        return {'overall_pick': overall_pick, 'round': adjusted_round, 'pick': adjusted_pick}

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


    def projections (self,content):
        '''
        Parses all rows of html table using BeautifulSoup and returns list of player dictionaries
        Args:
            content (str): html table typically fetched by FantasyCalculatorNFLScraper class
        Returns:
            List of dictionaries if successful, empty list otherwise.
        '''

        players = []
        headers = []

        soup = BeautifulSoup(content)
        table = soup.find('table', {'id': 'rankings-table'})

        for th in table.findAll('th'):
            value = th.string.lower()

            if re.match(r'\d+', value):
                headers.append('week%s_projection' % value)
            else:
                headers.append(value)

        headers = self.fix_headers(headers)

        # players - use regular expression to include header row (which has no class)
        for row in table.findAll('tr', {'class': re.compile(r'\w+')}):
            self.logger.debug(row)
            tds = [td.string for td in row.findAll("td")]
            player = dict(zip(headers, tds))

            # exclude unwanted positions from results
            if player.get('position') in self.positions:
                players.append(player)
            else:
                self.logger.info('excluded %s because %s' % (player.get('full_name'), player.get('position')))

        return players

if __name__ == '__main__':
    pass
    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #p = FantasyFootballCalculatorParser()
    #players = p.adp(my_league_size=16, content=content)
    #logging.info(pprint.pformat(players))
    
    '''
    import copy
    import xml.etree.ElementTree as ET

    with open('/home/sansbacon/players.xml', 'r') as infile:                                   
        tree = ET.parse(infile) 
        
    players = [node.attrib for node in tree.iter('player')] 
    fixed = []
    positions_wanted = ['QB', 'RB', 'WR', 'TE']

    for player in players:
        
        p = copy.deepcopy(player)
        
        # remove fields
        p.pop('twitter_username', None)
        p.pop('status', None)
            
        # convert birthdate from epoch
        try:
            p['birthdate'] = datetime.datetime.fromtimestamp(float(p.get('birthdate'))).strftime('%Y-%m-%d')
        except:
            p['birthdate'] = None

        # fix ffcalc_id
        try:
            ffcid = p.get('id')
            p['ffcalc_id'] = ffcid
        except:
            pass
        finally:
            p.pop('id', None)

        # fix nflcom_id
        try:
            nflid = p.get('nfl_id').split('/')[1]
            p['nflcom_id'] = nflid
        except:
            pass
        finally:
            p.pop('nfl_id', None)

        if p.get('position') in positions_wanted:
            fixed.append(p)
        
    print random.choice(fixed)
    '''
