from datetime import datetime
import logging
import time

from ewt.scraper import EWTScraper
from nflseasons import date_list, fantasylabs_week


class FantasyLabsNFLScraper(EWTScraper):
    '''
    FantasyLabsNFLScraper
    If you don't have a subscription, you can access the information freely-available on the website
    If you have a subscription, the scraper can use your firefox cookies and access protected content
    You cannot access protected content if you (a) have not logged in (b) have firefox open

    Usage:

        s = FantasyLabsNFLScraper()
        content = s.today()
        model = s.model('11_30_2016', 'levitan')
        models = s.models(seasons=range(2015,2017), weeks=range(1,18), model='levitan')
        
    '''

    def __init__(self, headers=None, cookies=None, cache_name=None):

        # see http://stackoverflow.com/questions/8134444
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        EWTScraper.__init__(self, headers=headers, cookies=cookies, cache_name=cache_name)

        self.headers = {'Referer': 'http://www.fantasylabs.com/nfl/player-models/',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'}

        self.model_urls = {
            'default': 'http://www.fantasylabs.com/api/playermodel/1/{model_date}/?modelId=47139',
            'levitan': 'http://www.fantasylabs.com/api/playermodel/1/{model_date}/?modelId=524658',
            'bales': 'http://www.fantasylabs.com/api/playermodel/1/{model_date}/?modelId=170627',
            'csuram': 'http://www.fantasylabs.com/api/playermodel/1/{model_date}/?modelId=193726',
            'tournament': 'http://www.fantasylabs.com/api/playermodel/1/{model_date}/?modelId=193746',
            'cash': 'http://www.fantasylabs.com/api/playermodel/1/{model_date}/?modelId=193745'
        }

    def games_day(self, game_date):
        '''
        Gets json for games on single date (can use any date in upcoming NFL week)

        Usage:
            content = s.game(game_date='10_04_2015')
            
        '''

        url = 'http://www.fantasylabs.com/api/sportevents/1/{0}'.format(game_date)
        content = self.get(url)

        if not content:
            logging.error('could not get content from url: {0}'.format(url))

        return content

    def games_days(self, start_date, end_date):
        '''
        Gets json for games in weeks that fall in date range

        Usage:
            games = s.games(start_date='10_04_2015', end_date='10_09_2015')
            
        '''

        contents = {}

        for d in date_list(end_date, start_date):
            datestr = datetime.strftime(d, '%m_%d_%Y')
            contents[datestr] = self.games_day(game_date=datestr)

        return contents

    def model(self, model_day, model_name='default'):
        '''
        Gets json for model, default to Bales model
        Stats in most models the same, main difference is the ranking based on weights of factors present in all models

        Arguments:
            model_day (str): in mm_dd_yyyy format
            model_name (str): uses default if not specified

        Returns:
            content (str): is json string

    	Arguments:
	        model_day(str): in %m_%d_%Y format
            model_name(str): default, bales, jennings, cash, tournament, etc.

        Usage:
            bales_model_json = s.model()
            csuram_model_json = s.model('csuram')

        '''

        content = None
        url = self.model_urls.get(model_name, None)

        if not url:
            logging.error('could not find url for {0} model'.format(model_name))
            url = self.model_urls.get('default')

        # have to add today's date in mm_dd_yyyy format to URL
        content = self.get(url.format(model_date=model_day))

    	if not content:
            logging.error('could not get content from url: {0}'.format(url))

        return content

    def models(self, seasons, weeks, model_name, polite=True):
        '''
        Stats in most models the same, main difference is the ranking based on weights of factors present in all models

        Usage:
            models = s.models(start_date='10_04_2015', end_date='10_09_2015', model_name='csuram')
            
        '''

        contents = {s:{w:'' for w in weeks} for s in seasons}

        for seas in seasons:
            for wk in weeks:
                contents[seas][wk] = self.model(model_day=fantasylabs_week(seas, wk))
                if polite:
                    time.sleep(2)

        return contents

if __name__ == "__main__":
    pass
