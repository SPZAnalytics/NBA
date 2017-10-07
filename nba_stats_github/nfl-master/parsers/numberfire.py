import logging
import os
import pprint
import re

from bs4 import BeautifulSoup

class NumberfireNFLParser():

    def __init__(self,**kwargs):

        if 'logger' in kwargs:
          self.logger = kwargs['logger']
        else:
          self.logger = logging.getLogger(__name__)

    def _player_link(self, link):
        player = {}
        
        # player position and team in parentheses -- >Ryan Tannehill (QB, MIA)</a>
        match = re.match(re.compile(r'\w+.*?\((\w+),\s+(\w+)\)'), link.string)
        if match:
            player['position'] = match.group(1).strip()
            player['team_id'] = match.group(2).strip()
    
        # player_id is last part of the href
        player['player_id'] = link['href'].split('/')[-1]
        
        return player

    def _player_row(self, tr):
        '''
        '''
        # <a href="/nfl/players/ryan-tannehill" rel="4461" title="Ryan Tannehill Fantasy Projection">Ryan Tannehill (QB, MIA)</a>
        link = tr.find('a')
        player = self._player_link(link)
        
        # now loop through <td> elements
        # want 1 - opponent, 2- opponent_rank, 3- overall_rank, 4- positional_rank
        tds = tr.findAll('td')
        
        # 1-2: opponent, opponent_rank (need to remove #)
        player['opponent'] = tds[1].string
        player['opponent_rank'] = tds[2].string.replace('#','')

        # 3-4: player ranks
        player['overall_rank'] = tds[3].string
        player['positional_rank'] = tds[4].string

        # 5-7: passing
        player['passing_yards'] = tds[5].string
        player['passing_tds'] = tds[6].string
        player['interceptions'] = tds[7].string
                
        # 8-10: rushing
        player['rushing_attempts'] = tds[8].string
        player['rushing_yards'] = tds[9].string
        player['rushing_tds'] = tds[10].string

        # 11-13: receiving
        player['receptions'] = tds[11].string
        player['receiving_yards'] = tds[12].string
        player['receiving_tds'] = tds[13].string

        # skip 14-17
        
        # 18-20 fanduel
        player['fanduel_points'] = tds[18].string
        player['fanduel_salary'] = tds[19].string
        player['fanduel_value'] = tds[20].string
        
        # 21-23 draftkings
        player['draftkings_points'] = tds[21].string
        player['draftkings_salary'] = tds[22].string
        player['draftkings_value'] = tds[23].string
        
        # last 3 yahoo
        player['yahoo_points'] = tds[-3].string
        player['yahoo_salary'] = tds[22].string
        player['yahoo_value'] = tds[23].string
       
        return player
           
    def projections (self, content):
        '''
        Parses numberfire HTML page into a list of player dictionaries
        :param content(string): html of numberfire nfl weekly page
        :return players(list): list of player dictionaries
        '''
    
        players = []

        soup = BeautifulSoup(content)
        table = soup.find('table', {'id': 'complete-projection'})

        # header rows have valign property, simplest way to filter out        
        for tr in table.findAll('tr', attrs={'valign': None}):
            players.append(self._player_row(tr))           

        return players

if __name__ == "__main__":
    
    with open(os.path.join(os.getenv("HOME"), 'numberfire-nfl.html')) as x: content = x.read()
    p = NumberfireNFLParser()
    pprint.pprint(p.projections(content))    

