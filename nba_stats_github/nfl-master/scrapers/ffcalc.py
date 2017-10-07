import logging
from urllib import urlencode

<<<<<<< HEAD
from ewt.scraper import EWTScraper
=======
from EWTScraper import EWTScraper
>>>>>>> ace1da00fd9afc9f38280055e9751ec1562994bb


class FantasyFootballCalculatorScraper(EWTScraper):
    '''
    Obtains html content of NFL fantasy projections or ADP page of fantasycalculator.com

    Example:
        s = FantasyCalculatorNFLScraper()
        content = s.get_projections()
        content = s.get_projections(url)
        content = s.get_projections(url, fn)
        
        content = s.get_adp()
        content = s.get_adp(url)
        content = s.get_adp(url, fn)
        
    '''

    def __init__(self, **kwargs):
        '''
        Args:
            **kwargs: projections_url (str)
        '''

        # see http://stackoverflow.com/questions/8134444/python-constructor-of-derived-class
        EWTScraper.__init__(self, **kwargs)

        if 'format' in 'kwargs':
            self.format = kwargs['format']
        else:
            self.format = 'standard'

        if 'projections_url' in 'kwargs':
            self.projections_url = kwargs['projections_url']
        else:
            self.projections_url = 'https://fantasyfootballcalculator.com/rankings'

        if 'teams' in 'kwargs':
            self.teams = kwargs['teams']
        else:
            self.teams = '14'

        if 'year' in 'kwargs':
            self.year = kwargs['year']
        else:
            self.year = '2015'

    def _adp_url(self):
        '''
        URL encode parameters for url for average draft position(ADP) page
        '''
        
        base_url = 'https://fantasyfootballcalculator.com/adp_xml.php?'

        params = {
            'format': self.format,
            'teams': self.teams,
        }

        url = base_url + urlencode(params)
        logging.debug('adp url is %s' % url)
        return url   

    def get_adp(self, url=None, fname=None):
        '''
        Fetch adp url, try cache, then file, then web
        Args:
            url (str): url for the fantasy football calculator ADP page
        Returns:
            Str if successful, None otherwise.
        '''

        if not url:
            url = self._adp_url()

        if not url and not fname:
            raise ValueError('invalid or missing URL or filename')

        return self.get(url, fname)

    def get_projections(self, url=None, fname=None):
        '''
        Fetch projections url, try cache, then file, then web
        Args:
            url (str): url for the fantasy football calculator projections page
        Returns:
            Str if successful, None otherwise.
        '''

        if not url:
            url = self.projections_url

        return self.get(url, fname)

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s = FantasyFootballCalculatorScraper()
    content = s.get_adp()
    logging.debug(content)
