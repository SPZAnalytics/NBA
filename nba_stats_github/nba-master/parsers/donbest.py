# -*- coding: utf-8*-
'''
'''
import logging
import re

from bs4 import BeautifulSoup


class DonBestNBAParser():
    '''
    import logging
    import os
    import pickle
    import time
    from nba.scrapers.donbest import DonBestNBAScraper
    from nba.parsers.donbest import DonBestNBAParser
    from nba.seasons import *

    logging.basicConfig(level=logging.DEBUG)
    s = DonBestNBAScraper(cache_name='odds')
    p = DonBestNBAParser()
    results = []

    for day in season_gamedays(2017, 'db'):
        try:
            content = s.odds(day)
            result = p.odds(content, day)
            results.append(result)
            time.sleep(2)
            logging.info('finished {}'.format(day))
        except Exception as e:
            logging.error('could not get odds for {}: {}'.format(day, e))
            continue

    with open(os.path.join(os.path.expanduser('~'), 'odds2017.pkl'), 'wb') as outfile:
        pickle.dump([item for sublist in results for item in sublist], outfile)
    '''

    def __init__(self):
        logging.getLogger(__name__).addHandler(logging.NullHandler())

    def _median(self, lst):
        lst = sorted(lst)
        if len(lst) < 1:
            return None
        if len(lst) % 2 == 1:
            return lst[((len(lst) + 1) / 2) - 1]
        else:
            return float(sum(lst[(len(lst) / 2) - 1:(len(lst) / 2) + 1])) / 2.0

    def _odds_total(self, x1, x2):
        '''
        Determines what is the spread and what is the total
        Args:
            x1: string
            x2: string

        Returns:
            (spread, total): floats or None if can't be determined
            order: either 'st', 'ts', None
        '''
        spread, total, order = (None, None, None)
        if x1 == 'PK':
            spread = 0
            total = float(x2)
            order = 'st'
        elif x2 == 'PK':
            spread = 0
            total = float(x1)
            order = 'ts'
        elif float(x1) > float(x2):
            spread = float(x2)
            total = float(x1)
            order = 'ts'
        else:
            spread = float(x1)
            total = float(x2)
            order = 'st'
        return (spread, total, order)

    def odds(self, content, game_date):
        '''
        Determines odds (for HOME team), total, and teams for one day of games

        Args:
            content: HTML string
            game_date: in %Y%m%d format

        Returns:
            results: list of odds dict. Odds always for HOME team.
        '''
        results = []
        soup = BeautifulSoup(content, 'lxml')

        for tr in soup.find_all('tr', {'class': re.compile(r'statistics_table')}):
            result = {'game_date': game_date}
            tds = tr.find_all('td')

            # this cell has the odds and game total, split by a <br>
            # there is no consistent order, odds or game total could be first
            ot = tds[1].find('div').decode_contents(formatter="html")
            x1, x2 = ot.split('<br/>')
            os, ot, order = self._odds_total(x1, x2)

            # team names are wrapped up in span element
            result['away'], result['home'] = [span.text for span in tds[2].find_all('span')]

            # spread always going to be set for the home team
            if order == 'st':
                result['opening_spread'] = 0 - os
            else:
                result['opening_spread'] = os

            result['opening_game_ou'] = ot

            # store casino spreads and totals
            cs = []
            ct = []

            # individual casino odds wrapped in <td><div></div><div></div></td>
            for td in tr.find_all('td', {'rel': re.compile(r'page\d+')}):
                x1, x2 = [e.text for e in td.find_all('div')]
                if x1 == 'PK':
                    x1 == 0
                elif x2 == 'PK':
                    x2 = 0

                # try/except protects against missing casino data: site uses '-' rather than empty string
                # can just skip it if can't convert to float
                if order == 'st':
                    try:
                        cs.append(0-float(x1))
                        ct.append(float(x2))
                    except:
                        logging.info('x1 is {} ({}) and x2 is {} ({})'.format(x1, type(x1), x2, type(x2)))

                elif order == 'ts':
                    try:
                        cs.append(float(x2))
                        ct.append(float(x1))
                    except:
                        logging.info('x1 is {} ({}) and x2 is {} ({})'.format(x1, type(x1), x2, type(x2)))

            # use median as consensus
            result['consensus_spread'] = self._median(cs)
            result['consensus_total'] = self._median(ct)
            results.append(result)

        return results

if __name__ == "__main__":
    pass