import copy
import logging
import os
import re

from bs4 import BeautifulSoup

class PfrNFLParser():
    '''
    PfrNFLParser

    Usage:


    '''

    def __init__(self,**kwargs):
        '''

        '''

        logging.getLogger(__name__).addHandler(logging.NullHandler())


    def _merge_team_tables(self, offense, passing, rushing):
        '''
        Takes 3 dictionaries (offense, passing, rushing), returns merged dictionary
        '''
        
        teams = copy.deepcopy(offense)

        for t in offense:
            p = passing.get(t)

        for k,v in p.items():
            teams[t][k] = v

            r = rushing.get(t)

        for k,v in r.items():
            teams[t][k] = v

        return teams

    def _season_from_path(self, path):
        '''Extracts 4-digit season from path, each html file begins with season'''

        fn = os.path.split(path)[-1]
        return fn[0:4]
                       
    def team_season(self, content, season):
        '''
        Takes HTML file of team stats during single season
        Returns dict, key is team_season, value is team
        '''

        soup = BeautifulSoup(content, 'lxml')   
        teams = {}
    
        offense = soup.find('table', {'id': 'team_stats'}).find('tbody')
        for tr in offense.findAll('tr'):
            team = {'season': season}
    
            for td in tr.findAll('td'):
                val = td.text
            
                # fix team name - has newline and extra space
                if '\n' in val:
                    val = ' '.join(val.split('\n'))
                    val = ' '.join(val.split())
                
                # column headers on page are duplicates (yds, td, etc.)    
                # data-stat attribute has accurate column name (rush_yds)
                team[td['data-stat']] = val
        
            k = team['team'] + "_" + season
            teams[k] = team

        passing = soup.find('table', {'id': 'passing'}).find('tbody')
        for tr in passing.findAll('tr'):
            team = {'season': season}
        
            for td in tr.findAll('td'):
                val = td.text
                
                # fix team name - has newline and extra space
                if '\n' in val:
                    val = ' '.join(val.split('\n'))
                    val = ' '.join(val.split())
                    
                # column headers on page are duplicates (yds, td, etc.)    
                # data-stat attribute has accurate column name (rush_yds)
                team[td['data-stat']] = val

            k = team['team'] + "_" + season
            teams[k] = {**teams[k], **team}

        rushing = soup.find('table', {'id': 'rushing'}).find('tbody')

        for tr in rushing.findAll('tr'):
            team = {'season': season}
        
            for td in tr.findAll('td'):
                val = td.text
                
                # fix team name - has newline and extra space
                if '\n' in val:
                    val = ' '.join(val.split('\n'))
                    val = ' '.join(val.split())
                    
                # column headers on page are duplicates (yds, td, etc.)    
                # data-stat attribute has accurate column name (rush_yds)
                team[td['data-stat']] = val

            k = team['team'] + "_" + season
            teams[k] = {**teams[k], **team}
            
        return teams


    def parse_season(self, content, season):
        soup = BeautifulSoup(content)

        players = []

        headers = [
            'rk', 'player', 'team', 'age', 'g', 'gs', 'pass_cmp', 'pass_att', 'pass_yds', 'pass_td', 'pass_int', 'rush_att',
            'rush_yds', 'rush_yds_per_att',
            'rush_td', 'targets', 'rec', 'rec_yds', 'rec_yds_per_rec', 'rec_td', 'fantasy_pos', 'fantasy_points',
            'draftkings_points', 'fanduel_points', 'vbd', 'fantasy_rank_pos', 'fantasy_rank_overall'
        ]

        t = soup.find('table', {'id': 'fantasy'})
        body = t.find('tbody')

        for row in body.findAll('tr'):
            values = [cell.text for cell in row.findAll('td')]

            # filter out header rows
            if 'Receiving' in values or 'Y/A' in values:
                continue

            player = (dict(zip(headers, values)))
            player['Season'] = season

            # fix *+ in name
            # add playerid
            link = row.find('a', href=re.compile(r'/players/'))

            if link:
                player['Player'] = link.text
                pid = link['href'].split('/')[-1]
                player['Id'] = pid[:-4]

            else:
                name = player.get('Player')
                if name:
                    name.replace('*', '')
                    name.replace('*', '+')
                    player['Player'] = name

            players.append(player)

        return players

if __name__ == "__main__":
    pass
