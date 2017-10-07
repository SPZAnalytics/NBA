# -*- coding: utf-8 -*-

import logging

import pandas as pd
import xlrd


class FootballOutsidersNFLParser2(object):

    '''
    Parses xls file of fantasy projections from footballoutsiders.com into player dictionaries

    Example:
        p = FootballOutsidersNFLParser(projections_file='KUBIAK.xls')
        players = p.projections()
    '''

    def __init__(self, projections_file, **kwargs):
        '''
        Args:
            projections_file(str)
            **kwargs: wanted_sheets(list of str): the sheets in the workbook you want to scrape
        '''

        self.projections_file = projections_file

        if 'wanted_cols' in 'kwargs':
            self.wanted_cols = kwargs['wanted_cols']
        else:
            self.wanted_cols = ['player', 'team', 'bye', 'pos', 'age', 'risk', 'dynamic fantasy points', 'position rank', 'auction value']

        if 'wanted_sheets' in 'kwargs':
            self.wanted_sheets = kwargs['wanted_sheets']
        else:
            self.wanted_sheets = ['2015 KUBIAK Projections']

    def _is_not_def(self, val):
        '''
        Exclude players of position IDP
        :param val:
        :return boolean:
        '''

        if val.lower() == 'd':
            return False
        else:
            return True

    def _is_not_idp(self, val):
        '''
        Exclude players of position IDP
        :param val:
        :return boolean:
        '''

        if 'IDP' in val:
            return False
        else:
            return True

    def _is_not_kicker(self, val):
        '''
        Exclude players of position IDP
        :param val:
        :return boolean:
        '''

        if val.lower() == 'k':
            return False
        else:
            return True

    def _parse_row(self, sheet, rowidx, column_map):
        '''
        Private method  
        :param sheet(xlrd worksheet object):
        :return players (list of dictionary):
        '''

        cells = []

        # loop through list of columns you want to scrape
        for column in self.wanted_cols:
            colidx = column_map.get(column, None)

            if colidx is not None:
                cell_value = str(sheet.cell(rowidx,colidx).value)
                cells.append(cell_value)
            else:
                logging.error('could not find column index for %s' % column)

        fixed_column_names = self._fix_headers(self.wanted_cols)
        player = dict(zip(fixed_column_names, cells))
        first_last, full_name = NameMatcher.fix_name(player['full_name'])
        player['first_last'] = first_last
        player['full_name'] = full_name
        logging.debug('player is %s' % player)
        return player

    def _parse_sheet(self, sheet):
        '''
        Private method  
        :param sheet(xlrd worksheet object):
        :return players (list of dictionary):
        '''

        players = []

        # get the column_map, key is name and value is index
        column_map = self._column_map(sheet)

        for rowidx in range(1, sheet.nrows):

            position_colidx = column_map.get('pos', None)
            position = str(sheet.cell(rowidx, position_colidx).value)

            if position_colidx:
                if self._is_not_idp(position) and self._is_not_kicker(position) and self._is_not_def(position):
                    player = self._parse_row(sheet=sheet, rowidx=rowidx, column_map=column_map)
                    players.append(player)
                else:
                    logging.debug('skipped %s' % position)
            else:
                logging.error('no position_colidx')

        return players

    def projections(self):
        '''

        :return players(list of dictionary): player dictionaries
        '''

        wb = xlrd.open_workbook(self.projections_file)

        players = []

        for sheet in wb.sheets():
            if sheet.name in self.wanted_sheets:
                players = players + self._parse_sheet(sheet)

        return players

    def _unwanted_columns(self):
        return ['Key', 'Picked', 'Rush', 'Ru', 'Rec', '300', '100', '100', 'Kick', 'XP', 'FG', 'FG Miss', 'Def',
                'Tot Tkl', 'Tkl', 'Ast', 'Sack', 'D-Int', 'Pass Def', 'Fum For', 'Fum Rec' , 'TD', '-',
                'Sack', 'D-Int', 'Fum Forc', 'Fum Recd', 'Saf', 'Def TD', 'Shut out', 'PA 1-6', 
                'PA 7-13', 'PA 14-20', 'PA 21-27', 'PA 28-34', 'PA 35+', 'NYA 0-199', 'NYA 200-249', 'NYA 259-299',
                'NYA 300-349', 'NYA 350-399', 'NYA 400-449', 'NYA 450-499', 'NYA 500+', '3 And Out', 'Spec Team',
                'Kick Ret Yds', 'Punt Ret Yds', 'Sp Team TDs', 'Other', 'Pass C%', 'YD/ATT', 'Net Y/P', 'YD/Run',
                'YD/Rec', '-', 'Risk', 'Playoff Adjust', 'Dynamic Fantasy Points', 'FPoints Over Baseline',
                'FPOB Rank', 'FPOB %', 'Position Rank', 'ESPN Rank', 'ESPN Delta', 'Yahoo Rank', 'Yahoo Delta',
                'ADP Rank', 'ADP Delta', 'FPOB Auction', 'Auction Value', 'Current Auction Value']
                
    def _fo_headers(self, header):
        ''',
        Standardizes headers from KUBIAK projections
        Assumes have already deleted unwanted columns
        '''

        fo = {
            'player': 'player_name',
            'fo id': 'site_player_id',
            'att': 'pass_att',
            'com': 'pass_cmp',
            'int': 'pass_int',
            'patd': 'pass_td',
            'payd': 'pass_yds',
            'pass dvoa': 'pass_dvoa',
            'rctd': 'rec_td',
            'rcyd': 'rec_yds',
            'rec dvoa': 'rec_dvoa',
            'rec c%': 'rec_cperc',
            'pass targets': 'pass_targets',
            'rutd': 'rush_td',
            'ruyd': 'rush_yds',
            'run dvoa': 'rush_dvoa',
            'fumb': 'fumbles'
        }
        
        return fo.get(header.lower(), header.lower())
        
    def fo(self,fn):
        try:
            df = pd.read_csv(fn)
            df.rename(columns=lambda x: _fo_headers(x), inplace=True)
            df['site'] = 'footballoutsiders'
            df.age = pd.to_numeric(df.age, errors='coerce')
            
            # percentage columns: pass_dvoa, rush_dvoa, rec_dvoa, rec_cperc
            for col in ['pass_dvoa', 'rush_dvoa', 'rec_dvoa', 'rec_cperc']:
                df[col] = df[col].apply(lambda x: str(x))     
                df[col] = df[col].apply(lambda x: float(x.strip('%'))/100)
            
            # fix nan
            df1 = df.where((pd.notnull(df)), None)
            
            # return list of dictionaries
            return df1[df1['pos'].isin(['QB', 'WR', 'TE', 'RB'])].T.to_dict().values()
           
        except Exception as e:
            logging.exception(e)
            return None
           
if __name__ == "__main__":
    main
