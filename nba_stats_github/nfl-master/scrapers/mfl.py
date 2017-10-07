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
        s = MyFantasyLeagueNFLScraper()
        players = s.get_players(positions=['QB', 'RB', 'WR', 'TE')
    '''

    def __init__(self, **kwargs):
        '''
        Args:
            **kwargs: projections_url (str)
        '''

        # see http://stackoverflow.com/questions/8134444/python-constructor-of-derived-class
        EWTScraper.__init__(self, **kwargs)

        self.players_url = 'http://football.myfantasyleague.com/2015/export?TYPE=players&DETAILS=1'
       
    def get_players(self, url=None, fname=None):
        '''
        Fetch players url, try cache, then file, then web
        Args:
            url (str): url for the players page
        Returns:
            Str if successful, None otherwise.
        '''

        return self.get(url, fname)

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s = MyFantasyLeagueNFLScraper()
    content = s.get_players()
    logging.debug(content)
