import datetime
import itertools
import logging
import time

import requests
import requests_cache

from nfl.parsers.fantasypros import FantasyProsNFLParser
from nfl.scrapers.fpros import FantasyProsNFLScraper
from nfl.nflseasons import get_season


class FantasyProsNFLAgent(object):
    '''
    Usage:
        import pickle
        logging.basicConfig(level=logging.INFO)
        a = FantasyProsNFLAgent()
        players = a.weekly_rankings_archived()
        with open('fpros-archive.pkl', 'wb') as outfile:
        pickle.dump(players, outfile)
    '''

    def __init__(self, wb=False):
        self._s = FantasyProsNFLScraper()
        self._p = FantasyProsNFLParser()
        if wb:
            requests_cache.install_cache('wb-fpros-cache')
        else:
            requests_cache.install_cache('fpros-cache')

    def _wb(self, fpros_url, d):
        '''
        Handles the wayback machine API
        Args:
            fpros_url (str): url of the page you want to look for
            d (date): date of beginning of nfl week

        Returns:
            content (str): the content from the wayback machine
        '''
        content = None
        cached = False
        base_wb = 'http://archive.org/wayback/available?url={}&timestamp={}'
        wb_url = base_wb.format(fpros_url, datetime.datetime.strftime(d, '%Y%m%d'))
        logging.info('wb_url is {}'.format(wb_url))

        r = requests.get(wb_url)
        r.raise_for_status()
        wb = r.json()

        # wb API tells if available and gives timestamp of page
        if wb['archived_snapshots']['closest']['available']:
            ts = wb['archived_snapshots']['closest']['timestamp']
            logging.info('ts is {}, t is {}'.format(ts, ts[:8]))
            ts = datetime.datetime.strptime(ts[:8], '%Y%m%d').date()
            cl_url = wb['archived_snapshots']['closest']['url']

            # need to match up the dates as best as possible
            delta = d - ts
            logging.info('d is {}'.format(datetime.datetime.strftime(d, '%Y-%m-%d')))
            logging.info('ts is {}'.format(datetime.datetime.strftime(ts, '%Y-%m-%d')))
            logging.info('delta is {}'.format(delta.days))
            if abs(delta.days) <= 5:
                r = requests.get(wb['archived_snapshots']['closest']['url'])
                r.raise_for_status()
                content = r.content
                if r.from_cache:
                    cached = True
                logging.info('delta days are {}'.format(delta.days))
            else:
                logging.error('page is too old')
        else:
            logging.error('url unavailable on wayback machine')

        return content, cached

    def weekly_rankings_archived(self):
        '''
        Gets old fantasypros rankings from the wayback machine
        Uses wayback API to figure out if week rankings exist, then fetch+parse result

        Returns:
            players(list): of player rankings dict
        '''
        players = []
        base_fpros = 'https://www.fantasypros.com/nfl/rankings/{}.php'
        positions = ['QB', 'RB', 'WR', 'TE']

        # loop through seasons
        for season in [2014, 2015]:

            # s is dict with keys = week, dict with keys start, end as value
            s = get_season(season)

            # loop through weeks
            for week, v in s.items():
                if s.get(week, None):
                    weekdate = s.get(week)
                    if weekdate:
                        d = weekdate.get('start')
                        logging.debug('d is a {}'.format(type(d)))
                    else:
                        raise Exception ('could not find start of {} week {}'.format(season, week))

                # loop through positions
                for pos in positions:

                    # generate url for wayback machine
                    fpros_url = base_fpros.format(pos)
                    content, cached = self._wb(fpros_url, d)

                    if content:
                        pw = self._p.weekly_rankings(content, season, week, pos)
                        logging.info(pw)
                        players.append(pw)
                    else:
                        logging.error('could not get {}|{}|{}'.format(season, week, pos))

                    if not cached:
                        time.sleep(2)

        # players is list of list, flatten at the end
        return list(itertools.chain.from_iterable(players))

    def weekly_rankings(self, season, week, flex=False):
        '''
        Gets current fantasypros rankings

        Returns:
            players(list): of player rankings dict
        '''
        players = []
        base_fpros = 'https://www.fantasypros.com/nfl/rankings/{}.php'
        positions = ['qb', 'rb', 'wr', 'te', 'flex']

        # loop through seasons
        # loop through positions
        for pos in positions:
            if not flex and pos == 'flex':
                continue

            content = self._s.get(base_fpros.format(pos))

            if content:
                pw = self._p.weekly_rankings(content, season, week, pos)
                logging.info(pw)
                players.append(pw)
            else:
                logging.error('could not get {}|{}|{}'.format(season, week, pos))

        # players is list of list, flatten at the end
        if not flex:
            return list(itertools.chain.from_iterable(players))
        else:
            return list(itertools.chain.from_iterable(players)), flex_players

if __name__ == '__main__':
    pass
