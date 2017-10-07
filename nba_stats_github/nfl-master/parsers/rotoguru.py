import copy
import logging

from bs4 import BeautifulSoup


class RotoguruNFLParser():
    '''
    RotoguruNFLParser

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

        pass
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
        '''

    def _split(self, pre):
        vals = []
        rows = pre.splitlines()
        headers = rows.pop(0).split(';')
        
        for row in rows:
            vals.append(dict(zip(headers, row.split(';'))))

        return vals
        
    def parse(self, content):
        soup = BeautifulSoup(content, 'lxml')
        for pre in soup.findAll('pre'):
            if 'Week;Year' in pre.text:
                return self._split(pre.text)
            else:
                raise Exception('no pre in content')
        
    def _fix(self, players):
        '''
        TODO: figure out what this does
        I think it was an ad hoc fix to a problem with the parse routine
        '''
        fixed = []

        for player in players:              
            fp = {}
            fp['source'] = 'rotoguru' 
            fp['source_player_id'] = player.get('GID')
            fp['dfs_site'] = 'dk'
            fp['player'] = player.get('Name')
            fp['season'] = player.get('Year')
            fp['week'] = player.get('Week')
            fp['team'] = player.get('Team').upper()
            fp['opp'] = player.get('Oppt').upper()
            fp['pos'] = player.get('Pos')
            
            sal = player.get('DK salary', 0)
            try:
                sal = int(sal)
            except:
                sal = 0
            fp['salary'] = sal        
            cp = player.get('DK points')
            if cp: fp['curr_points'] = cp
            fp['is_home'] = True if player.get('h/a') == 'h' else False
            
            if fp.get('salary', 0) > 0:
                fixed.append(fp)
        
        return fixed
        
if __name__ == "__main__":
    pass
