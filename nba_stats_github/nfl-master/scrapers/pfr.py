'''
PfrNFLScraper

'''

import logging

from ewt.scraper import EWTScraper


class PfrNFLScraper(EWTScraper):
    '''
    Usage:
        s = RotoguruNFLScraper()

    '''

    def __init__(self, **kwargs):

        # see http://stackoverflow.com/questions/8134444
        EWTScraper.__init__(self, **kwargs)
        self.logger = logging.getLogger(__name__).addHandler(logging.NullHandler())
        self.pgl_finder_url = 'http://www.pro-football-reference.com/play-index/pgl_finder.cgi'

        if 'polite' in 'kwargs':
            self.polite = kwargs['polite']
        else:
            self.polite = True

        if 'params' in 'kwargs':
            self.params = kwargs['params']
        else:
            self.params = {
                'request':1, 'match':'game', 'year_min': 2016, 'year_max': 2016, 'season_start':1, 'season_end':-1, 'age_min':0, 'age_max':0, 'pos': '', 'game_type':'R',
                'career_game_num_min':0, 'career_game_num_max':499, 'game_num_min':0, 'game_num_max':99, 'week_num_min': 1, 'week_num_max': 17, 'c1stat':'choose', 'c1comp':'gt',
                'c2stat':'choose', 'c2comp':'gt', 'c3stat':'choose', 'c3comp':'gt', 'c4stat':'choose', 'c4comp':'gt', 'c5comp':'choose', 'c5gtlt':'lt', 'c6mult':1.0, 'c6comp':'choose',
                'offset': 0, 'order_by':'draftkings_points'
            }

    def _week_position(self, season, week, pos, offsets=[0, 100, 200]):
        '''
        Gets one week of fantasy stats for one position
        '''

        results = []

        # pfr only shows 100 per page - not a problem for QB but
        # need 2nd page for TE and 3rd page for WR and RB
        for offset in offsets:
            params = self.params
            if pos == 'QB' and offset > 0:
                continue
            elif pos == 'TE' and offset > 100:
                continue
            else:
                params['year_min'] = season
                params['year_max'] = season
                params['week_num_min'] = week
                params['week_num_max'] = week
                params['pos'] = pos
                if offset > 0: params['offset'] = offset
                content = self.get(self.pgl_finder_url, params=params)
                if content: results.append(content)

        return results

    def week_positions(self, season, week, positions=['QB', 'RB', 'WR', 'TE'], slp=2):
        '''
        Gets one week of fantasy stats for all positions
        '''
        results = {p:'' for p in positions}
        for pos in positions:
            results[pos] = self._week_position(season, week, pos)

        return results

if __name__ == "__main__":
    pass
