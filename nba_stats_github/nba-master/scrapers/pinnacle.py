'''
PinnacleNBAScraper.py
Gets daily odds xml feed from pinnacle sports
http://xml.pinnaclesports.com/pinnaclefeed.aspx?sporttype=Basketball&sportsubtype=nba
'''
import logging

from ewt.scraper import EWTScraper

from nba.scrapers.scraper import BasketballScraper


class PinnacleNBAScraper(BasketballScraper):
    '''
    Gets daily nba game/odds xml feed from pinnacle sports
    '''

    def __init__(self, headers=None, cookies=None, cache_name=None):
        '''

        Args:
            headers:
            cookies:
            cache_name:
        '''
        # see http://stackoverflow.com/questions/8134444
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        BasketballScraper.__init__(self, headers, cookies, cache_name)
        self.odds_url = 'http://xml.pinnaclesports.com/pinnaclefeed.aspx?sporttype=Basketball'

    def odds(self):
        return self.get(self.odds_url)

if __name__ == "__main__":
    pass
