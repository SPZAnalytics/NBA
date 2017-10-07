'''
ESPNNBAScraper
'''

import logging
import os
import re
import time

from bs4 import BeautifulSoup

from nba.scrapers.scraper import BasketballScraper


class ESPNNBAScraper(BasketballScraper):
    '''

    '''

    def __init__(self, headers=None, cookies=None, cache_name=None):

        # see http://stackoverflow.com/questions/8134444
        logging.getLogger(__name__).addHandler(logging.NullHandler())

        if not headers:
            self.headers = {'Referer': 'http://www.fantasylabs.com/nfl/player-models/',
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        else:
            self.headers = headers

        self.cookies = cookies
        self.cache_name = cache_name

        BasketballScraper.__init__(self, headers=self.headers, cookies=self.cookies, cache_name=self.cache_name)

        self.maxindex = 400
        base_url = 'http://games.espn.go.com/ffl/tools/projections?'
        idx = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360]
        self.projection_urls = [base_url + 'startIndex=' + x for x in idx]

    def player_page(self, content):

        # <td align="left"><a href="http://espn.go.com/nba/player/_/id/110/kobe-bryant">Kobe Bryant</a>

        players = {}
        soup = BeautifulSoup(content)
        pattern = re.compile('player/_/id/(\d+)/(\w+[^\s]*)', re.IGNORECASE)
        links = soup.findAll('a', href=pattern)

        for link in links:
            match = re.search(pattern, link['href'])

            if match:
                players[match.group(1)] = match.group(2)

            else:
                logging.error('could not get {0}'.format(link['href']))

        return players

    def players(self):

        # now get all of the player pages
        base_url = 'http://stats.nba.com/stats/commonplayerinfo?PlayerID='
        ids = [p['PERSON_ID'] for p in players]
        for id in ids:

            # create url
            url = base_url + str(id)
            logging.debug('url is ' + url)

            # create filename
            fn = os.path.join(expanduser("~"), savedir, str(id) + '.json')
            logging.debug('filename is ' + fn)

            # get the resource
            resp, content = h.request(url, "GET")
            logging.debug('status is ' + str(resp.status))

            # if request is success, then save resource to file
            if resp.status == 200:
                try:
                    with open(fn, 'w') as outfile:
                        outfile.write(content)
                        logging.debug('saved player ' + str(id) + ' to ' + fn)
                except:
                    logging.exception('could not save file ' + fn)

        return content

    def projections(self, subset=None):
        pages = []
        if subset:
            for idx in subset:
                content = self.get(self.projection_urls[idx])
                pages.append(content)
        else:
            for url in self.projection_urls:
                content = self.get(url)
                pages.append(content)

        return pages


class FiveThirtyEightNBAScraper(EWTScraper):
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
        BasketballScraper.__init__(self, headers=self.headers, cookies=self.cookies, cache_name=self.cache_name)

    def espn_player_ids(self, pklfname=None):

        # this is a list of lists
        all_players = {}

        page_numbers = range(1, 11)

        for page_number in page_numbers:
            url = 'http://espn.go.com/nba/salaries/_/page/{0}/seasontype/1'.format(page_number)
            content = self.get(url)
            players = player_page(content)
            for id, name in players.items():
                all_players[id] = name

        if pklfname:
            with open(pklfname, 'w') as outfile:
                json.dump(all_players, outfile, indent=4, sort_keys=True)

        return all_players

    def fivethirtyeight_nba(self, pklfname, savedir):

        # get player_ids
        with open(pklfname, 'r') as infile:
            espn_players = json.load(infile)

        for player_code in espn_players.values():
            player_code = re.sub('[.\']', '', player_code)
            fn = os.path.join(savedir, '{0}.json'.format(player_code))

            if os.path.isfile(fn):
                logging.debug('already have {0}'.format(fn))

            else:
                if len(player_code) > 3:
                    content, from_cache = simscores(player_code)

                    if content:
                        with open(fn, 'w') as outfile:
                            outfile.write(content)
                    else:
                        logging.debug('could not get {0}'.format(player_code))

                    if from_cache:
                        logging.debug('got url from cache')

                    else:
                        time.sleep(2)

                else:
                    logging.debug('could not get {0}'.format(player_code))

    def simscores(self, player_code):
        url = 'http://projects.fivethirtyeight.com/carmelo/{0}.json'.format(player_code)

        try:
            content = self.get(url)
            return content

        except:
            logging.exception('could not get {0}'.format(url))
            return None


if __name__ == "__main__":
    pass

    '''
    import logging
    import re
    import time

    from bs4 import BeautifulSoup
    from ewt.scraper import EWTScraper

    s = EWTScraper(cache_name='espn-nba')

    teams_page = 'http://www.espn.com/nba/teams'
    players = []
    teams = {}

    tpcontent = s.get(teams_page)
    soup = BeautifulSoup(tpcontent, 'lxml')

    for teama in soup.find_all('a', {'href': re.compile(r'/nba/teams/roster')}):
        roster_url = 'http://espn.go.com' + teama['href']
        team_code = roster_url.split('=')[-1]
        teams[team_code] = {'url': roster_url, 'name': teama.text}

        content = s.get(roster_url)
        tsoup = BeautifulSoup(content, 'lxml')

        for tr in tsoup.find_all('tr', {'class': re.compile(r'player-\d+')}):

            # get player name and id
            espn_player_id, espn_player_url = (None, None)
            links = [td.find('a') for td in tr.find_all('td') if td.find('a')]
            if links:
                url = links[0]['href']
                if url:
                    espn_player_url = url
                    match = re.search(r'/id/(\d+)/(\w+-\w+)', url)
                    if match:
                        espn_player_id = match.group(1)

            # 0 jersey, 1 name, 2 position, 3 age, 4 height, 5 weight, 6 college, 7 salary
            headers = ['jersey', 'espn_player_name', 'espn_position', 'age', 'height', 'weight', 'college', 'nba_salary']
            tds = [td.text for td in tr.find_all('td')]
            player = dict(zip(headers, tds))
            player['espn_player_url'] = espn_player_url
            player['espn_player_id'] = espn_player_id
            players.append(player)

        time.sleep(2)

    print players
    print teams
    '''
