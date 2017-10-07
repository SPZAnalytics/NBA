from __future__ import print_function

import logging
import string

from nba.scrapers.scraper import BasketballScraper


class BBRefScraper(BasketballScraper):
    '''
    Usage:
        s = BBRefScraper()
    '''

    def __init__(self, headers=None, cookies=None, cache_name=None):
        '''

        Args:
            headers:
            cookies:
            cache_name:
        '''
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        BasketballScraper.__init__(self, headers=headers, cookies=cookies, cache_name=cache_name)

    def players(self):
        '''

        Returns:
            content: dict with keys of alphabet
        '''

        base_url = 'http://www.basketball-reference.com/players/{}/'

        content = {}
        for l in string.ascii_lowercase:
            try:
                content[l] = self.get(base_url.format(l))
            except:
                continue
        '''
            soup = BeautifulSoup(content, 'lxml')
            t = soup.find('table', {'id': 'players'})
            tb = t.find('tbody')
            for tr in tb.find_all('tr'):
                vals = {td['data-stat']: td.text for td in tr.find_all('td')}

                th = tr.find('th')
                if th.find('strong'):
                    vals['active'] = True
                else:
                    vals['active'] = False

                if th.find('a'):
                    a = th.find('a')
                    vals['player_name'] = a.text
                    vals['player_url'] = a['href']

                players.append(vals)
        '''

if __name__ == "__main__":
    pass