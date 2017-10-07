import collections
import logging

class NFLProjectionsParser:

    '''
    Generic NFL parser. Is a base class.

    Example:
	No examples - should subclass
    '''

    def __init__(self, **kwargs):
        '''

        :param kwargs:
        :return:
        '''

    def _column_map(self, s):
        '''
        Creates a dictionary of column names and indexes
        :param s(xlrd spreadsheet object):
        :return column_map(OrderedDictionary): mapping of columns to scrape with their index numbers
        '''

    	# standardize on lowercase column names
        column_map = collections.OrderedDict()

        for colidx in range(s.ncols):
            colname = str(s.cell(0,colidx).value).lower().strip()
            column_map[colname] = colidx

        return column_map

    def _fix_header(self, header):
        '''
        Standardizes headers/keys used on various fantasy sites
        :param header (str):
        :return fixed_header (str):
        '''

        fixed_headers = {
            'auction': 'auction_value',
            'auction value': 'auction_value',
            'avg rank': 'average_rank',
            'best rank': 'best_rank',
            'bye week': 'bye',
            'byeWeek': 'bye',
            'display_name': 'full_name',
            'displayName': 'full_name',
            'draft slot': 'tier',
            'dynamic fantasy points': 'fantasy_points',
            'espn rank': 'espn_rank',
            'fantasy color grade': 'color',
            'name': 'full_name',
            'overallRank': 'overall_rank',
            'player': 'full_name',
            'player name': 'full_name',
            'pos': 'position',
            'position rank': 'position_rank',
            'positionRank': 'position_rank',
            'pts': 'fantasy_points',
            'standDev': 'stdev_rank',
            'std dev': 'stdev_rank',
            'wild card': 'wild_card',
            'worst rank': 'worst_rank',
            'yahoo rank': 'yahoo_rank',
        }

        return fixed_headers.get(header, None)

    def _fix_headers(self, headers):
        '''
        Standardize team codes, relies on _fix_team_code
        :param headers(list): the original keys/headers
        :return fixed_headers(list): the standardized keys/headers
        '''
        fixed_headers = []

        for header in headers:
            fixed_header = self._fix_header(header.lower())

            if fixed_header:
                fixed_headers.append(fixed_header)
            else:
                fixed_headers.append(header)

        return fixed_headers
        
    def _fix_team_code(self, team_name):
        '''
        Standardizes NFL team codes, takes city or other code
        :param team_name(str): could be Seattle Seahawks or Arizona
        :return team_code(str): standardized 2- or 3-digit code for team
        '''

        team_codes = {
            'Arizona': 'ARI', 'Atlanta': 'ATL',
            'Baltimore': 'BAL', 'Buffalo': 'BUF',
            'Carolina': 'CAR', 'Chicago': 'CHI',
            'Cincinnati': 'CIN', 'Cleveland': 'CLE',
            'Dallas': 'DAL', 'Denver': 'DEN',
            'Detroit': 'DET', 'Green Bay': 'GB',
            'Houston': 'HOU', 'Indianapolis': 'IND',
            'Jacksonville': 'JAC', 'Kansas City': 'KC',
            'Miami': 'MIA', 'Minnesota': 'MIN',
            'New England': 'NE', 'New Orleans': 'NO',
            'NY Giants': 'NYG', 'NY Jets': 'NYJ',
            'Oakland': 'OAK', 'Philadelphia': 'PHI',
            'Pittsburgh': 'PIT', 'San Diego': 'SD',
            'San Francisco': 'SF', 'Seattle': 'SEA',
            'St. Louis': 'STL', 'Tampa Bay': 'TB',
            'Tennessee': 'TEN', 'Washington': 'WAS',
            'JACK': 'JAC', 'WSH': 'WAS',
            'Cardinals': 'ARI', 'Falcons': 'ATL',
            'Ravens': 'BAL', 'Bills': 'BUF',
            'Panthers': 'CAR', 'Bears': 'CHI',
            'Bengals': 'CIN', 'Browns': 'CLE',
            'Cowboys': 'DAL', 'Broncos': 'DEN',
            'Lions': 'DET', 'Packers': 'GB',
            'Texans': 'HOU', 'Colts': 'IND',
            'Jaguars': 'JAC', 'Chiefs': 'KC',
            'Dolphins': 'MIA', 'Vikings': 'MIN',
            'Patriots': 'NE', 'Saints': 'NO',
            'Giants': 'NYG', 'Jets': 'NYJ',
            'Raiders': 'OAK', 'Eagles': 'PHI',
            'Steelers': 'PIT', 'Chargers': 'SD',
            '49ers': 'SF', 'Seahawks': 'SEA',
            'Rams': 'STL', 'Buccaneers': 'TB',
            'Titans': 'TEN', 'Redskins': 'WAS',
            'Buffalo Bills': 'BUF', 'Seattle Seahawks': 'SEA',
            'Philadelphia Eagles': 'PHI', 'St. Louis Rams': 'STL',
            'Arizona Cardinals': 'ARI', 'Carolina Panthers': 'CAR',
            'Green Bay Packers': 'GB', 'New England Patriots': 'NE',
            'Dallas Cowboys': 'DAL', 'Detroit Lions': 'DET',
            'Kansas City Chiefs': 'KAN', 'Houston Texans': 'HOU',
            'Baltimore Ravens': 'BAL', 'New York Giants': 'NYG',
            'Denver Broncos': 'DEN', 'Chicago Bears': 'CHI',
            'Miami Dolphins': 'MIA', 'San Francisco 49ers': 'SAN',
            'Cincinnati Bengals': 'CIN', 'Cleveland Browns': 'CLE',
            'Indianapolis Colts': 'IND', 'Minnesota Vikings': 'MIN',
            'Washington Redskins': 'WAS', 'Jacksonville Jaguars': 'JAC',
            'Pittsburgh Steelers': 'PIT', 'Atlanta Falcons': 'ATL',
            'New Orleans Saints': 'NO', 'Tennessee Titans': 'TEN',
            'Tampa Bay Buccaneers': 'TB', 'New York Jets': 'NYJ',
            'Oakland Raiders': 'OAK', 'San Diego Chargers': 'SD',
        }

        return team_codes.get(team_name, team_name)

    def _fix_team_codes(self, team_names):
        '''
        Standardize team codes, relies on _fix_team_code
        :param team_names(list):
        :return list:
        '''
        return [self._fix_team_code(team_name) for team_name in team_names]

    def _is_not_dst(val):
        '''
        Tests whether player is position player or team defense
        :param val(str): the position
        :return (boolean): true if not defense, false if defense
        '''

        if 'D-ST' in val:
            return False

        else:
            return True

    def _player_id(self, name):
        '''
        Creates player_id if one does not exist
        :param name(str): assumes in First Last format
        :return player_id(str): returns in First_Last format
        '''

        return name.replace(' ', '_')

if __name__ == '__main__':
    pass
