import logging

from ewt.scraper import EWTScraper


class FantasyProsNFLScraper(EWTScraper):

    '''
    '''
    def __init__(self, headers=None, cookies=None, cache_name=None):
        
        logging.getLogger(__name__).addHandler(logging.NullHandler())

        if not headers:
            self.headers = {'Referer': 'http://www.fantasylabs.com/nfl/player-models/',
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        else:
            self.headers = headers

        self.cookies = cookies
        self.cache_name = cache_name

        EWTScraper.__init__(self, headers=self.headers, cookies=self.cookies, cache_name=self.cache_name)

        self.adp_url = 'http://www.fantasypros.com/nfl/adp/overall.php?export=xls'
        self.projection_url = 'http://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php?export=xls'

    def get_adp(self, fname=None):
        if not fname:
            return self._get(self.adp_url)

        else:
            tmp_fname, headers = self.get_file(self.adp_url, fname)
            logging.debug('get_adp: http response headers')
            logging.debug(headers)
            return tmp_fname

    def get_season_rankings(self, fname=None):
        pass

    def get_projections(self, fname=None):
        '''
        Download csv file and save to specified or temporary location if no fname parameter
        :param fname (str): specified location to save file
        :return tmp_fname (str), headers(dict)
        '''

        if not fname:
            return self.get(self.projection_url)

        else:
            tmp_fname, headers = self.get_file(self.projection_url, fname)
            logging.debug('get_projections: http response headers')
            logging.debug(headers)
            return tmp_fname

if __name__ == "__main__":
    pass
