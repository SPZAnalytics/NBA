import copy
import json
import logging

from bs4 import BeautifulSoup

from nfl.parsers import projections


class ProFootballFocusNFLParser():
    '''
    ProFootballFocusNFLParser

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
        
if __name__ == "__main__":
    pass
