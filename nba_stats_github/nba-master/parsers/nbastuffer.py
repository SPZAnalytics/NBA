import logging
import re

from nba.teams import NBATeamNames


class NBAStufferParser(object):

    '''
    Parses xls or csv file of NBA game info from nbastuffer.com into game dictionaries

    Example:
        p = NBAStufferParser()
        fn='stuffer.xlsx'
        wb = xlrd.open_workbook(fn)
        sheet = wb.sheet_by_index(0)
        if sheet:
            games = p.xlsx_game_pairs(sheet, p.xlsx_headers(sheet))
    
    '''

    def __init__(self, nbadotcom_games = {}, omit = None):
        '''
        Args:
            nbadotcom_games (dict): key-value pair of gamecode and nbacom_game_id
            omit (list): fields to omit from nbastuffer files
        '''

        logging.getLogger(__name__).addHandler(logging.NullHandler())
        logging.addHandler(logging.NullHandler())

        self.names = NBATeamNames()
        self.nbadotcom_games = nbadotcom_games

        if omit:
            self.omit = omit
        else:
            self.omit = ['teams', 'f', 'moneyline', 'moneyline_', 'movements', 'opening_odds', 'to to']

    def _fix_headers(self, headers_):
        '''
        Standardize with field names used by nba.com

        Args:
            headers_ (list):

        Returns:
            fixed (list):
        '''

        fixed = []

        convert = {
            'date': 'gamedate',
            'team_abbreviation': 'team_code',
            'fg': 'fgm',
            'ft': 'ftm',
            'dr': 'dreb',
            'or': 'oreb',
            'tot': 'reb',
            'a': 'ast',
            'st': 'stl',
            'bl': 'blk',
            'to': 'tov',
            '3p': 'fg3m',
            '3pa': 'fg3a',
            'spread': 'opening_spread',
            'total': 'opening_total'
        }

        for header in headers_:
            converted = convert.get(header, None)

            if converted:
                fixed.append(converted)

            else:
                fixed.append(header)

        return fixed

    def _fix_new_orleans(self, gamecode, season):
        '''
        Inconsistent naming of New orleans pelicans / hornets / oklahoma city (katrina year)
        This produces the correct 3-letter code to match up to nba.com gamecodes

        Args:
            gamecode (str): 20151031/CHINOP
            season (str): 2015-16

        Returns:
            gamecode (str):
        '''

        if season in ['2007', '2008', '2009', '2010', '2011', '2012']:
            return gamecode.replace('NOP', 'NOH')

        elif season in ['2005', '2006']:
            return gamecode.replace('NOP', 'NOK')

        else:
            return gamecode

    def _fix_starters(self, *args):
        '''
        Removes strange unicode characters in some of the player (starter) fields

        Args:
            variable length list of strings

        Returns:
            fixed (list): strings with unicode characters removed
        '''

        fixed = []
        
        for team in args:
            for k in team:
                if 'starter' in k:
                    team[k] = team[k].replace('\xc2\xa0', '')

            fixed.append(team)
            
        return fixed
        
    def _gameid(self, gamecode, dataset='Regular'):
        '''
        Takes gamecode and returns game_id used by nba.com

        Args:
            gamecode(str): format 20151027/CLECHI.
            dataset (str): name of dataset (regular season or playoff)

        Returns:
            gameid (str): 8 or 10-digit gamecode

        '''
        game = self.nbadotcom_games.get(gamecode)
        gameid = None

        if game:
            gameid = game.get('game_id', None)
            logging.debug('_gameid returns {0}'.format(gameid))

        else:
            # right now, don't have playoffs in games database, no need to print all of those errors
            if 'Regular' in dataset:
                logging.warning('_gameid: could not find id for gamecode {0}'.format(gamecode))
    
            else:
                logging.debug('_gameid: could not find id for playoff gamecode {0}'.format(gamecode))
            
        return gameid

    def _gamecode(self, away, home):
        '''
        Returns gamecode based on game_pair from nbastuffer dataset
        Game_pair is a list with two elements: first is dictionary of away team, second is dictionary of home team

        Args:
            away (dict): top row in game_pair
            home (dict): bottom row in game_pair

        Returns:
             gamecode (str): in format 20141031/CHICLE

        '''

        gamecode = None
        gamedate = away.get('gamedate', None)
        
        away_team = away.get('team_code', None)
        home_team = home.get('team_code', None)

        if gamedate and away_team and home_team:
            match = re.search(r'(\d+)\/(\d+)\/(\d+)', gamedate)
            
            if match:
                if len(match.group(3)) > 2:
                    gamecode = '{0}{1}{2}/{3}{4}'.format(match.group(3), match.group(1), match.group(2), away_team, home_team)
                    #logging.debug('gamecode: {0}'.format(gamecode))
                else:
                    gamecode = '20{0}{1}{2}/{3}{4}'.format(match.group(3), match.group(1), match.group(2), away_team, home_team)
                    #logging.debug('gamecode: {0}'.format(gamecode))

            else:
                gamecode = '{0}/{1}{2}'.format(gamedate, away_team, home_team)

        # new orleans pelicans / hornets / oklahoma city (katrina year) fix
        if gamecode and 'NOP' in gamecode:
            season = away.get('dataset', 'XXXX')[0:4]
            gamecode = self._fix_new_orleans(gamecode, season)

        logging.debug('_gamecode returns {0}'.format(gamecode))
        return gamecode

    def _get_closing(self, team1, team2, rowidx=0):
        '''
        Takes 2 team dictionaries, extracts cell with closing odds / closing (could be line or spread) or sets to None

        Args:
            team1 (dict):
            team2 (dict):
            rowidx (int):

        Returns:
            team1_odds (str):
            team2_odds (str):

        Examples:
            Various formats:
                Sometimes total like 198
                Sometimes + odds like 7
                Sometimes - odds like -7
                Sometimes a hybrid like -5.5 -05
                Sometimes includes PK (which is Pick'Em, 0 spread)
                Sometimes looks like -1.5-05
        '''
        
        team1_odds = team1.get('closing_odds', None)
        team2_odds = team2.get('closing_odds', None)
        
        # odds are stored under 'closing_odds' and 'closing' depending on the year
        if team1_odds == None or team1_odds == '':
            team1_odds = team1.get('closing', None)

            # if can't get closing, rely on opening
            if team1_odds == None or team1_odds == '':
                team1_odds = team1.get('spread', None)
                team2_odds = team1.get('total', None)
                logging.error('have to rely on opening odds: {0}, {1}: {2}'.format(team2.get('gamedate', 'Gamedate N/A'), team1.get('teams', 'Team N/A'), team2.get('teams', 'Team N/A')))

        # odds are stored under 'closing_odds' and 'closing' depending on the year
        if team2_odds == None or team1_odds == '':
            team2_odds = team2.get('closing', None)

            if team2_odds == None or team1_odds == '':
                team2_odds = team2.get('total', None)
                team1_odds = team1.get('spread', None)
                logging.error('have to rely on opening odds: {0}, {1}: {2}'.format(team2.get('gamedate', 'Gamedate N/A'), team1.get('teams', 'Team N/A'), team2.get('teams', 'Team N/A')))

        # if can't obtain anything, then skip further processing on odds
        if team1_odds == None or team1_odds == '':
            logging.error('error _get_closing: line %d | team1_odds: %s  team2_odds %s' % (rowidx, team1_odds, team2_odds))

        elif team2_odds == None or team1_odds == '':
            logging.error('error _get_closing: line %d | team1_odds: %s  team2_odds %s' % (rowidx, team1_odds, team2_odds))

        else:
            '''
            Takes 2 team dictionaries, extracts cell with closing odds / closing (could be line or spread) or sets to None
            Various formats:
                Sometimes a hybrid like -5.5 -05
                Sometimes includes PK (which is Pick'Em, 0 spread)
                Sometimes looks like -1.5-05
            '''

            # remove PK and set to zero
            if 'PK' in team1_odds:
                team1_odds = 0

            # otherwise strip out multiple odds if present
            else:
                match = re.search(r'([-]?\d+\.?\d?)\s?.*?', team1_odds)

                if match:
                    team1_odds = match.group(1)

            # remove PK and set to zero
            if 'PK' in team2_odds:
                team2_odds = 0

            # otherwise strip out multiple odds if present
            else:
                match = re.search(r'([-]?\d+\.?\d?)\s?.*?', team2_odds)

                if match:
                    team2_odds = match.group(1)

        logging.debug('team odds: {0}, {1}: {2}, {3}'.format(team1.get('teams', 'Team N/A'), team2.get('teams', 'Team N/A'), team1_odds, team2_odds))
               
        return team1_odds, team2_odds

    def _implied_total(self, game_total, spread):
        '''
        Takes game total and spread and returns implied total based on those values

        Args:
            game_total (float): something like 201.5
            spread (float): something like -1.5

        Returns:
            implied_total (float): something like 100.25
        '''

        try:
            return (float(game_total)/float(2)) - (float(spread)/float(2))

        except TypeError as e:
            logging.error('implied total error: {0}'.format(e.message))
            return None
                
    def _is_total_or_spread(self, val1, val2):
        '''
        Tests if it is a game total or a point spread; former is always larger

        Args:
            val1 (float):
            val2 (float):

        Returns:
            val_type (str): 'total' or 'spread'
        '''

        try:
            if float(val1) > float(val2):
                return 'total'
            else:
                return 'spread'

        except:
            logging.error('{0} or {1} is not a number'.format(val1, val2))
            return None

    def _point_spread(self, odds):
        '''
        Takes point spread, can be negative or positive, assumes that spread is for team1

        Args:
            odds (float):

        Returns:
            team1_spread (float):
            team2_spread (float):
        '''

        try:
            return float(odds), 0 - float(odds)

        except Exception as e:
            logging.exception(e.message)
            return None, None

    def _rest(self, team):
        '''
        `days_last_game` tinyint not null,
        `back_to_back` bool not null,
        `back_to_back_to_back` bool not null,
        `three_in_four` bool not null,
        `four_in_five` bool not null,
        3+, B2B, B2B2B, 3IN4, 3IN4-B2B, 4IN5, 4IN5-B2B

        '''

        team['days_last_game'] = None
        rest_days = team.get('rest_days', None)
        
        if rest_days is not None:

            # B2B and B2B2B
            if 'B2B' in rest_days:
                team['back_to_back'] = True
                team['days_last_game'] = 0
            else:
                team['back_to_back'] = False

            if 'B2B2B' in rest_days:
                team['back_to_back_to_back'] = True
            else:
                team['back_to_back_to_back'] = False

            # 3IN4
            if '3IN4' in rest_days:
                team['three_in_four'] = True
                team['days_last_game'] = 1
            else:
                team['three_in_four'] = False

            # 4IN5
            if '4IN5' in rest_days:
                team['three_in_four'] = True
                team['four_in_five'] = True
                team['days_last_game'] = 0

            else:
                team['four_in_five'] = False

            if re.match(r'\d{1}', rest_days):
                team['days_last_game'] = rest_days[0]

        return team

    def _team_abbrev(self, team_name):
        '''
        NBAStuffer uses the city name only, not the team name, which is annoying b/c New Orleans / Charlotte multiple teams over time
        '''
        
        return self.names.city_to_code(team_name)

    def _total_and_spread(self, team1, team2, rowidx):
        '''
        Spreadsheet/csv has odds in an inconsistent format, so have to wrangle to make it uniform
        Returns game_ou, away_spread, home_spread
        '''

        # team1_odds, team2_odds are in -8 195 format (depending on whether total or spread
        # type will be "total" or "spread"
        team1_odds, team2_odds = self._get_closing(team1, team2, rowidx)
        logging.info('team1 odds: {}'.format(team1_odds))
        logging.info('team2 odds: {}'.format(team2_odds))
        team1_type = self._is_total_or_spread(team1_odds, team2_odds)

        game_ou = None
        away_spread = None
        home_spread = None

        if team1_odds is not None and team2_odds is not None:
            # if team1_odds is total, then team2_odds is spread
            # set the game_ou and then calculate spreads
            if team1_type == 'total':       
                game_ou = team1_odds
                home_spread, away_spread = self._point_spread(team2_odds)
                
            # if team1_odds is a spread,
            # calculate spreads for both teams and then set the game_ou
            elif team1_type == 'spread':
                away_spread, home_spread = self._point_spread(team1_odds)
                game_ou = team2_odds
                
            else:
                logging.error('row {0}: not spread or line - {1} {2}'.format(rowidx, team1_odds, team2_odds))

        else:
            logging.error('row {0}: not spread or line - {1} {2}'.format(rowidx, team1_odds, team2_odds))
       
        return game_ou, away_spread, home_spread

    def game_pairs(self, rows, headers):
        '''
        Goes through data rows two at a time (grouped by home/away team in same game)
        Returns list of (list of 2 dictionaries (home and away info) that represents one game)

        Args:
            rows (list): lines from csv file
            headers (list): headers for each row

        Returns:
            gp (list): each game pair is a list of 2 teams that played in game
        '''

        gp = []
        
        for rowidx in range(0,len(rows),2):
            # merge all of the cells in the row with the headers
            # proceed in pairs because 2 rows make for one game

            team1 = dict(list(zip(headers, rows[rowidx].split(','))))
            team2 = dict(list(zip(headers, rows[rowidx+1].split(','))))
            team1, team2 = self._fix_starters(team1, team2)

            if team1 and team2:
                # convert team city to 3-letter code
                # add codes to both teams in game_pair
                team1['team_code'] = self._team_abbrev(team1.get('teams', None))
                team2['team_code'] = self._team_abbrev(team2.get('teams', None))
                team1['opponent_team_code'] = team2['team_code']
                team2['opponent_team_code'] = team1['team_code']
                team1['away_team'] = team1['team_code']
                team1['home_team'] = team2['team_code']
                team2['away_team'] = team1['team_code']
                team2['home_team'] = team2['team_code']

                # team ids
                team1['team_id'] = self.names.code_to_id(team1['team_code'])
                team2['team_id'] = self.names.code_to_id(team2['team_code'])
                team1['opponent_team_id'] = self.names.code_to_id(team1['opponent_team_code'])
                team2['opponent_team_id'] = self.names.code_to_id(team2['opponent_team_code'])
                team1['away_team_id'] = self.names.code_to_id(team1['away_team'])
                team2['away_team_id'] = self.names.code_to_id(team2['away_team'])
                team1['home_team_id'] = self.names.code_to_id(team1['home_team'])
                team2['home_team_id'] = self.names.code_to_id(team2['home_team'])

                # opponent points
                team1['opponent_points'] = team2['pts']
                team2['opponent_points'] = team1['pts']
                
                # spread and totals will be 196, -8 or -8, 196
                # add game_ou, away_spread, home_spread to both teams in game_pair
                game_ou, away_spread, home_spread = self._total_and_spread(team1, team2, rowidx)
                team1['game_ou'] = game_ou
                team1['away_spread'] = away_spread
                team1['home_spread'] = home_spread

                away_implied_total = self._implied_total(game_ou, away_spread)
                home_implied_total = self._implied_total(game_ou, home_spread)

                team1['away_implied_total'] = away_implied_total
                team1['home_implied_total'] = home_implied_total
                team2['game_ou'] = game_ou
                team2['away_spread'] = away_spread
                team2['home_spread'] = home_spread
                team2['away_implied_total'] = away_implied_total
                team2['home_implied_total'] = home_implied_total

                # gamecode is in 20151030/DETCHI
                # gameid is nbadotcom identifier for games
                gamecode = self._gamecode(team1, team2)
                game_id = self._gameid(gamecode, team1.get('dataset', 'Regular'))
                team1['gamecode'] = gamecode
                team2['gamecode'] = gamecode
                team1['game_id'] = game_id
                team2['game_id'] = game_id

                # rest
                team1 = self._rest(team1)
                team2 = self._rest(team2)

                # fix closing
                if 'closing' in team1:
                    team1['closing_odds'] = team1['closing']
                    team1.pop('closing')

                if 'closing' in team2:
                    team2['closing_odds'] = team2['closing']
                    team2.pop('closing')

                # fix gamedate
                if 'gamedate' in team1:
                    team1['game_date'] = team1['gamedate']
                    team1.pop('gamedate')

                if 'gamedate' in team2:
                    team2['game_date'] = team2['gamedate']
                    team2.pop('gamedate')

                # regular season
                if 'Regular' in team1['dataset']:
                    team1['is_regular_season'] = True
                    team2['is_regular_season'] = True

                # overtime
                if team1.get('ot1'):
                    team1['has_ot'] = True
                    team2['has_ot'] = True

                # omit some fields - can pass parameter or use defaults
                for field in self.omit:
                    team1.pop(field.lower(), None)
                    team2.pop(field.lower(), None)
                    team1.pop(field.upper(), None)
                    team2.pop(field.upper(), None)

                gp.append([team1, team2])

            else:
                logging.error('could not get team1 or team2')

        return gp

    def headers(self, row):
        '''
        Takes first row of sheet or csv file and returns lowercase column header with no spaces
        '''

        return self._fix_headers([re.sub(r'\s+', '_', c).strip().lower() for c in row])
        
    def xlsx_game_pairs(self, sheet, headers):
        '''
        Goes through data rows two at a time (grouped by home/away team in same game)
        Returns list of (list of 2 dictionaries (home and away info) that represents one game)
        '''
        
        gp = []
        
        for rowidx in range(1,sheet.nrows,2):
            team1 = dict(list(zip(headers, rows[rowidx])))
            team2 = dict(list(zip(headers, rows[rowidx+1])))

            if team1 and team2:
                # convert team city to 3-letter code
                team1['team_code'] = self._team_abbrev(team1.get('teams', None))
                team2['team_code'] = self._team_abbrev(team2.get('teams', None))
                team1['away_team'] = team1['team_code']
                team1['home_team'] = team2['team_code']
                team2['away_team'] = team1['team_code']
                team2['home_team'] = team2['team_code']

                # spread and totals will be 196, -8 or -8, 196
                game_ou, away_spread, home_spread = self._total_and_spread(team1, team2, rowidx)
                team1['game_ou'] = game_ou
                team1['away_spread'] = away_spread
                team1['home_spread'] = home_spread
                team2['game_ou'] = game_ou
                team2['away_spread'] = away_spread
                team2['home_spread'] = home_spread

                # gamecode is in 20151030/DETCHI
                # gameid is nbadotcom identifier for games
                gamecode = self._gamecode(game_pair)
                game_id = self._gameid(gamecode)
                team1['gamecode'] = gamecode
                team2['gamecode'] = gamecode
                team1['game_id'] = game_id
                team2['game_id'] = game_id
                team2['gamecode'] = gamecode

                # rest
                team1 = self._rest(team1)
                team2 = self._rest(team2)

                gp.append([team1, team2])

            else:
                logging.error('%s | row %d: could not get team1 or team2 - %s' % (sheet.name, rowidx))

        return gp

    def xlsx_headers(self, sheet):
        '''
        Takes first row of sheet and returns lowercase column header with no spaces
        Still need to address issue of starting players, format in spreadsheet is off
        '''

        _headers = []

        for colidx in range(0, sheet.ncols):
            header = sheet.cell(0, colidx).value.strip()
            header = re.sub(r'\s+', '_', header)

            if header == '':
                header = 'starting_lineups'

            _headers.append(header.lower())

        return _headers

if __name__ == "__main__":
    import glob
    import pprint
    import random

    from nba.db.pgsql import NBAPostgres

    logging.basicConfig(level=logging.ERROR)
    p = NBAStufferParser()
    db = NBAPostgres()

    fixed_games = []

    for fn in glob.glob('/home/sansbacon/workspace/nba-data/nbastuffer/csv/*Box*.csv'):

        with open(fn, 'r') as infile:
            rows = infile.readlines()

        headers = rows.pop(0).split(',')
        headers = p.headers(headers)
        game_pairs = p.game_pairs(rows, headers)

        wanted = ['is_regular_season', 'has_ot', 'dataset', 'game_date', 'venue', 'rest_days', 'days_last_game', 'back_to_back', 'back_to_back_to_back',
                  'three_in_four', 'four_in_five', 'gamecode', 'team_code', 'team_id', 'opponent_team_code', 'opponent_team_id',
                  'q1', 'q2', 'q3', 'q4', 'ot1', 'ot2', 'ot3', 'ot4',
                  'away_team', 'away_team_id', 'home_team', 'home_team_id',
                  'has_ot', 'poss', 'pts', 'opponent_points', 'pace', 'deff', 'oeff', 'opening_spread', 'opening_total', 'closing_odds',
                  'game_ou', 'away_spread', 'home_spread', 'away_implied_total', 'home_implied_total']

        for game_pair in game_pairs:
            for game in game_pair:
                fixed_game = {k:v for k,v in game.items() if k in wanted}

                for k,v in fixed_game.items():
                    if v == '':
                        fixed_game[k] = None

                fixed_games.append(fixed_game)

    db.insert_dicts(fixed_games, 'dfs.nbastuffer_boxes')

    '''
    import csv
    with open('nbastuffer.csv') as f:
        meta = [{k:v for k, v in row.items()}
             for row in csv.DictReader(f, skipinitialspace=True)]

    for idx, m in enumerate(meta):
        for k,v in m.items():
            if v == '':
                meta[idx][k] = None
            elif v == 'Not available':
                meta[idx][k] = None
            elif isint(v):
                meta[idx][k] = int(v)
            elif isfloat(v):
                meta[idx][k] = float(v)
    '''