'''
RotoguruNFLScraper

'''

import logging

from ewt.scraper import EWTScraper


class RotoguruNFLScraper(EWTScraper):
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
        Gets rotoguru page of one week of dfs results - goes back to 2014
        '''
        
        contents = {}
        base_url = 'http://rotoguru1.com/cgi-bin/fyday.pl?week={week}&year={year}&game={site}&scsv=1'

        for site in sites:
            url = base_url.format(week=week, year=year, site=site)                 
            contents[site] = self.get(url)
                    
        return contents

    def dfs_weeks(self, years, weeks, sites):
        '''
        Gets rotoguru page of range of weeks of dfs results - goes back to 2014
        '''
        
        contents = {}
        base_url = 'http://rotoguru1.com/cgi-bin/fyday.pl?week={week}&year={year}&game={site}&scsv=1'

        for site in sites:
            contents[site] = {}
            
            for year in years:
                contents[site][year] = {}
                
                for week in weeks:
                    url = base_url.format(week=week, year=year, site=site)                 
                    contents[site][year][week] = self.get(url)
                    
        return contents

if __name__ == "__main__":
    pass
