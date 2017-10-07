'''
NFLDotComScraper

'''

from bs4 import BeautifulSoup
import logging
import re
import time

from ewt.scraper import EWTScraper


class NFLDotComScraper(EWTScraper):
    '''
    Usage:
        s = NFLDotComScraper()
        game_ids = s.week_pages(season=2015, start_week=1, end_week=13)

    '''

    def __init__(self, **kwargs):
        # see http://stackoverflow.com/questions/8134444
        EWTScraper.__init__(self, **kwargs)
        self.logger = logging.getLogger(__name__).addHandler(logging.NullHandler())

        if 'polite' in 'kwargs':
            self.polite = kwargs['polite']
        else:
            self.polite = True

    def gamecenter(self, game_id, save=False):
        
        url = 'http://www.nfl.com/liveupdate/game-center/{0}/{0}_gtd.json'.format(game_id)
        logging.debug(url)
        content = self.get(url)

        if content and save:
            fname = url.split('/')[-1]
            self._to_file(fname=fname, content=content)

        if self.polite:
            time.sleep(6)
        else:
            time.sleep(3)

    def _week_page(self, url, save=False):
        '''
        Parses a weekly page with links to individual gamecenters
        :param url(str):
        :param save(bool):
        :return:
        '''
        game_ids = []
        content = self.get(url)

        if content:

            match = re.search(r'http://www.nfl.com/scores/(\d+)/(REG\d+)', url)

            if save and match:
                fname = match.group(1) + '_' + match.group(2) + '.html'
                self._to_file(fname=fname, content=content)

            soup = BeautifulSoup(content)

            for a in soup.findAll('a', class_='game-center-link'):
                # <a href="/gamecenter/2014090400/2014/REG1/packers@seahawks" class="game-center-link" . . . </a>
                game_url = a['href']
                pattern = re.compile(r'/gamecenter/(\d+)/\d+/REG')

                match = re.search(pattern, game_url)

                if match:
                    game_ids.append(match.group(1))

        return game_ids
    
    def week_pages(self, season, start_week=None, end_week=None, save=False):
        '''
        Gets weekly pages and returns all game_ids, which can be used to scrape gamecenters.
        Default is entire season, can pick one or more weeks also.
        :param season(int): the season year (2015, for example)
        :param start_week(int): Number from 1-17
        :param end_week(int): Number from 1-17
        :return:
        '''
        game_ids = []
        
        if start_week and end_week:
            weeks = range(start_week, end_week + 1)
        elif start_week:
            weeks = range(start_week, 18)
        elif end_week:
            weeks = range(1, end_week + 1)
        else:
            weeks = range(1, 18)

        for week in weeks:
            url = 'http://www.nfl.com/scores/{0}/REG{1}'.format(season, str(week))
            game_ids += self._week_page(url=url, save=save)

            if self.polite:
                time.sleep(4)
            else:
                time.sleep(2)
          
        return game_ids

if __name__ == "__main__":
    pass
