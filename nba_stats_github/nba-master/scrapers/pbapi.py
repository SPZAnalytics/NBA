import logging

from ewt.scraper import EWTScraper

class ProBasketballAPIScraper(EWTScraper):

    def __init__(self, api_key):
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        self.urls = {
            'players': 'https://probasketballapi.com/draftkings/players'
        }

        self.api_key = api_key

    def players(self):

        payload = {
            'api_key': self.api_key
        }

        r = self.post(url=self.urls.get('players'), params=payload)
        return r.json()