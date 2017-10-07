'''
RotowireNFLScraper

'''

import logging
import re

<<<<<<< HEAD
from ewt.scraper import EWTScraper
=======
from EWTScraper import EWTScraper
>>>>>>> ace1da00fd9afc9f38280055e9751ec1562994bb


class RotowireNFLScraper(EWTScraper):
    '''
    Usage:
        s = RotoguruNFLScraper()

    '''

    def __init__(self, **kwargs):
        # see http://stackoverflow.com/questions/8134444
        EWTScraper.__init__(self, **kwargs)
        self.logger = logging.getLogger(__name__).addHandler(logging.NullHandler())

        if 'polite' in 'kwargs':
            self.polite = kwargs['polite']
        else:
            self.polite = True

    def dfs_week(self, year, week, sites):
        '''
        Gets rotowire page of one week of dfs results
        '''
        
        url = 'http://www.rotowire.com/daily/nfl/value-report.php?site=DraftKings'
        return self.get(url)

if __name__ == "__main__":
    pass
