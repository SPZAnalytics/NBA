from collections import defaultdict
import logging

from bs4 import BeautifulSoup as bs
from nfl.teams import city_to_code


class FootballLocksNFLParser():
    '''
    FootballLocksNFLParser

    Usage:

    '''

    def __init__(self):
        '''

        '''
        logging.getLogger(__name__).addHandler(logging.NullHandler())

    def _fix_odds(self, o):
        '''

        Args:
            o(dict): dictionary of odds

        Returns:
            o(dict): add keys to dict

        '''
        fav = o.get('favorite')
        dog = o.get('underdog')

        # tot won't convert if empty
        tot = o.get('total', 0)
        try:
            tot = float(tot)
        except:
            tot = 0
        o['game_total'] = tot

        # spread won't convert if PK or empty
        spread = o.get('spread', 0)
        if spread == 'PK' or spread == '':
            spread = 0
        else:
            try:
                spread = float(spread)
            except:
                spread = 0
        o['spread'] = spread

        # home favorite has 'At' before city name
        if 'At' in fav:
            home_team = ' '.join(fav.split(' ')[1:])
            away_team = dog
            home_total = self._implied_total(tot, spread)
            away_total = tot - home_total

        else:
            away_team = fav
            home_team = ' '.join(dog.split(' ')[1:])
            away_total = self._implied_total(tot, spread)
            home_total = tot - away_total

        o['home_team'] = city_to_code(home_team)
        o['away_team'] = city_to_code(away_team)
        o['home_implied'] = home_total
        o['away_implied'] = away_total

        wanted = ['season_year', 'week', 'dt', 'away_team', 'home_team', 'away_implied', 'home_implied', 'game_total', 'spread', 'money_odds']
        return {k:v for k,v in o.items() if k in wanted}

    def _implied_total(self, game_total, spread):
        '''
        Takes game total and spread and returns implied total based on those values

        Args:
            game_total (float): something like 53.5
            spread (float): something like -1.5

        Returns:
            implied_total (float): something like 27.5
        '''

        try:
            return (float(game_total) / 2) - (float(spread) / 2)

        except TypeError, e:
            logging.error('implied total error: {0}'.format(e.message))
            return None

    def odds(self, content, season_start, week):
        '''
        Parses HTML page of odds
        Args:
            content(str): page for week of odds, has several years in separate tables

        Returns:

        '''
        season = season_start
        results = []
        soup = bs(content, 'lxml')

        # there are 2 different kinds of tables: main slate & MNF except for week 17
        # that is why I need to process main + MNF as a pair
        tables = soup.find_all('table', {'cols': '6', 'cellspacing': '6'})
        headers = ['dt', 'favorite', 'spread', 'underdog', 'total', 'money_odds']

        if week == 17:
            for t in tables:
                for tr in t.find_all('tr')[1:]:
                    val = dict(zip(headers, [td.text.strip() for td in tr.find_all('td')]))
                    val['season_year'] = season_start
                    val['week'] = week
                    results.append(self._fix_odds(val))
                    season -= 1

        else:
            i = 0
            while i < len(tables):
                # do the main table first
                main = tables[i]
                for tr in main.find_all('tr')[1:]:
                    val = dict(zip(headers, [td.text.strip() for td in tr.find_all('td')]))
                    val['season_year'] = season
                    val['week'] = week
                    results.append(self._fix_odds(val))

                mnf = tables[i + 1]
                for tr in mnf.find_all('tr'):
                    val = dict(zip(headers, [td.text.strip() for td in tr.find_all('td')]))
                    val['season_year'] = season
                    val['week'] = week
                    results.append(self._fix_odds(val))

                i += 2
                season -= 1

        return results

if __name__ == "__main__":
    import logging
    import pickle
    import pprint
    import random
    import time

    import requests
    import requests_cache

    from nfl.parsers.footballlocks import FootballLocksNFLParser
    from nfl.db.nflpg import NFLPostgres

    logging.basicConfig(level=logging.ERROR)
    requests_cache.install_cache('odds')
    parser = FootballLocksNFLParser()
    base_url = 'http://www.footballlocks.com/nfl_odds_week_{}.shtml'

    odds = []
    for week in range(1, 18):
        r = requests.get(base_url.format(week))
        r.raise_for_status()
        odds.append(parser.odds(r.content, 2016, week))
        if not r.from_cache:
            time.sleep(2)
    odds = [item for sublist in odds for item in sublist]
    nflp = NFLPostgres(user='postgres', password='cft091146', database='nfldb')
    nflp.insert_dicts(odds, 'odds')

    #with open('/home/sansbacon/odds.pkl', 'wb') as outfile:
    #    pickle.dump(odds, outfile)