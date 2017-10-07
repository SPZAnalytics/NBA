import collections
import logging
import pprint
from xlrd import open_workbook

class FootballScientistParser:

    '''
    Parses xlsx file of fantasy projections from thefootballscientist.com into player dictionaries

    Example:
        p = FootballScientistParser(projections_file='fs.xlsx')
        players = p.projections()
    '''

    def __init__(self, projections_file, **kwargs):
        '''
        Args:
            projections_file(str)
            **kwargs: wanted_sheets(list of str): the sheets in the workbook you want to scrape
        '''

        self.projections_file = projections_file

        if 'transformed_cols' in 'kwargs':
            self.transformed_cols = kwargs['transformed_cols']
        else:
            self.transformed_cols = {'rank': 'pos_rank', 'bye week': 'bye', 'fantasy color grade': 'color', 'draft slot': 'tier'}

        if 'wanted_cols' in 'kwargs':
            self.wanted_cols = kwargs['wanted_cols']
        else:
            self.wanted_cols = ['rank', 'player', 'team', 'pos', 'fantasy color grade', 'bye week', 'draft slot', 'auction']

        if 'wanted_sheets' in 'kwargs':
            self.wanted_sheets = kwargs['wanted_sheets']
        else:
            self.wanted_sheets = ['QB cheat sheet', 'RB cheat sheet', 'WR cheat sheet', 'TE cheat sheet', 'D-ST cheat sheet']

    def _column_headers(self, s):

        '''
        Args:
            s(xlrd spreadsheet object)

        Returns:
             OrderedDict: mapping of columns to scrape with their index numbers
        '''

        colnames = {str(s.cell(0,colidx).value).lower().strip(): colidx  for colidx in range(s.ncols)}

        #for colidx in range(s.ncols):
        #    colname = str(s.cell(0,colidx).value).lower().strip()
        #    colnames[colname] = colidx

        # now create ordered dictionary of the columns I want and the respective index
        wanted_cols_od = collections.OrderedDict()

        # now handle the rest of the columns
        for wcn in self.wanted_cols:

            idx = colnames.get(wcn, None)
            if idx == None:
                logging.warn('%s: no column %s' % (s.name, wcn))

            else:
                # transform column names
                transformed = self.transformed_cols.get(wcn, None)
                if transformed:
                    wanted_cols_od[transformed.strip()] = idx
                else:
                    wanted_cols_od[wcn.strip()] = idx

        return wanted_cols_od

    def _fix_team_code(self, team_name):
        '''

        :param team_name (str):
        :return team_code (str):
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
            'JACK': 'JAC', 'WSH': 'WAS'
        }

        return team_codes.get(team_name, team_name)

    def _is_not_dst(val):

        if 'D-ST' in val:
            return False

        else:
            return True


    def _parse_row(self, sheet, wanted_columns):

        player = {'pos': pos}

        for colname, colidx in wanted_columns.items():

            if colname in ['bye', 'age']:
                try:
                    player[colname] = (str(int(s.cell(rowidx,colidx).value)))
                except:
                    player[colname] = (str(s.cell(rowidx,colidx).value))

            elif colname == 'player':
                player_name = str(s.cell(rowidx,colidx).value)
                player['id'] = self._player_id(player_name).lower()
                player['player'] = player_name

            elif colname == 'team':
                team_name = str(s.cell(rowidx,colidx).value)
                team_code = self._fix_team_code(team_name)

                if 'D-ST' in s.name:
                    player['team'] = team_code
                    player['name'] = team_code + "_DST"
                    player['id'] = self._player_id(player['name']).lower()
                else:
                    player['team'] = team_code

            else:
                player[colname] = (str(s.cell(rowidx,colidx).value))

        return player


    def _parse_sheet(self, sheet):
        '''

        :param sheet(xlrd worksheet object):
        :return players (list of dictionary):
        '''

        players = []

        # get values from the wanted columns
        wanted_columns = self._column_headers(sheet)

        # add position for sheet, extracted from sheet name
        pos = sheet.name.split()[0].strip().lower()

        # loop over all the non-header rows in the sheet
        for rowidx in range(1,sheet.nrows):

            player = {'pos': pos}

            for colname, colidx in wanted_columns.items():

                if colname in ['bye', 'age']:
                    try:
                        player[colname] = (str(int(sheet.cell(rowidx,colidx).value)))
                    except:
                        player[colname] = (str(sheet.cell(rowidx,colidx).value))

                elif colname == 'player':
                    player_name = str(sheet.cell(rowidx,colidx).value)
                    player['id'] = self._player_id(player_name).lower()
                    player['player'] = player_name

                elif colname == 'team':
                    team_name = str(sheet.cell(rowidx,colidx).value)
                    team_code = self._fix_team_code(team_name)

                    if 'D-ST' in sheet.name:
                        player['team'] = team_code
                        player['name'] = team_code + "_DST"
                        player['id'] = self._player_id(player['name']).lower()
                    else:
                        player['team'] = team_code

                else:
                    player[colname] = (str(sheet.cell(rowidx,colidx).value))

            players.append(player)

        return players


    def _player_id(self, name):
        '''

        :param name (str):
        :return id (str):
        '''

        return name.replace(' ', '_')

    def projections(self):
        '''

        :return players(list of dictionary): player dictionaries
        '''

        wb = open_workbook(self.projections_file)
        players = []

        for sheet in wb.sheets():
            if sheet.name in self.wanted_sheets:
                players = players + self._parse_sheet(sheet)

        return players

if __name__ == '__main__':

    p = FootballScientistParser(projections_file='tfs.xlsx')
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.debug(pprint.pformat(p))
    #pprint.pprint(p.projections())