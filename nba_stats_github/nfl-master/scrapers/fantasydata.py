'''
FantasyDataNFLScraper.py
http://www.fantasydata.com
'''

<<<<<<< HEAD
from ewt.scraper import EWTScraper
=======
from EWTScraper import EWTScraper
>>>>>>> ace1da00fd9afc9f38280055e9751ec1562994bb
import logging

class FantasyDataNFLScraper(EWTScraper):
    '''
    Gets daily nba game/odds xml feed from pinnacle sports
    '''

    def __init__(self, **kwargs):
        '''
        EWTScraper parameters: 'dldir', 'expire_time', 'headers', 'keyprefix', 'mc', 'use_cache'
        '''

        # see http://stackoverflow.com/questions/8134444
        EWTScraper.__init__(self, expire_time=300, **kwargs)

        logging.getLogger(__name__).addHandler(logging.NullHandler())

        if 'odds_url' in kwargs:
            self.odds_url = kwargs['odds_url']
        else:
            self.odds_url = 'http://xml.pinnaclesports.com/pinnaclefeed.aspx?sporttype=Football&sportsubtype=nfl&contest=no'

    def salaries(self):
        url = '''https://fantasydata.com/nfl-stats/daily-fantasy-football-salary-and-projection-tool.aspx?fs=1&stype=0&sn=0&scope=0&w=0&ew=0&s=&t=0&p=1&st=FantasyPointsDraftKings&d=1&ls=FantasyPointsDraftKings&live=false&pid=false&minsnaps=4'''

if __name__ == "__main__":
    pass
