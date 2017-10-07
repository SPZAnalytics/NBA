from datetime import datetime
import logging

from nba.scrapers.scraper import BasketballScraper


class RotoGuruNBAScraper(BasketballScraper):
    '''

    Usage:
        s = RotoGuruNBAScraper()
        print s.salaries_day('2015-12-09', 'dk')
        print s.data_day(day=datetime.strftime(datetime(2015,12,9,0,0), '%Y%m%d'))

    '''

    def __init__(self, headers=None, cookies=None, cache_name=None):
        '''

        Args:
            headers:
            cookies:
            cache_name:
        '''
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        # see http://stackoverflow.com/questions/8134444
        BasketballScraper.__init__(self, headers, cookies, cache_name)
        
    def data_day(self, day, extra_params=None):
        '''
        TODO: needs a better name
        http://rotoguru1.com/cgi-bin/hoopstat-daterange.pl?
        gameday=20141228&tmptmax=999&date=20141228&ha=&opptmax=999&saldate=20141228&
        opptmin=0&startdate=20141228&g=0&min=&gmptmax=999&gmptmin=0&tmptmin=0&sd=0
        '''

        # default
        content = None

        # will add query string later
        base_url = 'http://rotoguru1.com/cgi-bin/hoopstat-daterange.pl?'

        # if caller does not pass params, these are what are used in query string
        default_params = {
            'startdate': day,
            'date': day,
            'saldate': day,
            'g': 0,
            'gameday': day,
            'ha': '',
            'min': '',
            'tmptmin': 0,
            'tmptmax': 999,
            'opptmin': 0,
            'opptmax': 999,
            'gmptmin': 0,
            'gmptmax': 999,
            'sd': 0
        }

        # merge params with base if passed when called
        if extra_params:
            z = default_params
            z.update(extra_params)
            params = z
        else:
            params = default_params

        content = self.get(url=base_url, payload=params)

        if not content:
            logging.error('data_day: could not get {0}'.format(url))

        return content

    def salaries_day(self, sday, site):

        # default
        content = None

        # need to use datetime object if pass string
        if isinstance(sday, basestring):
            sday = datetime.strptime(sday, '%Y%m%d')

        # will add query string later
        base_url = 'http://rotoguru1.com/cgi-bin/hyday.pl?'

        # if caller does not pass params, these are what are used in query string
        params = {
            'game': site,
            'mon': sday.month,
            'day': sday.day,
            'year': sday.year,
            'scsv': '1'
        }

        content = self.get(url=base_url, payload=params)

        if not content:
            logging.error('salaries_day: could not get {0}'.format(url))
            
        return content

if __name__ == "__main__":   
    pass
