'''
PinnacleNBAParser.py
http://xml.pinnaclesports.com/pinnaclefeed.aspx?sporttype=Basketball&sportsubtype=nba
'''

from datetime import datetime
from dateutil import tz
import logging
from operator import itemgetter
import pprint

from bs4 import BeautifulSoup

from nba.teams import NBATeamNames


class PinnacleNBAParser(object):
    '''
    Takes xml from scraper, returns list of game dictionaries

    Usage:
        p = PinnacleNBAParser()

        with open('/home/sansbacon/1.xml', 'r') as infile:
            xml = infile.read()

            - OR -

        s = PinnacleNBAScraper()
        xml = s.odds()
        games = p.odds(xml)
        p.to_csv(games, date)
        p.to_tsv(games, date)
        p.to_fw(games, date)

    '''

    def __init__(self, **kwargs):

        logging.getLogger(__name__).addHandler(logging.NullHandler())

        if 'game_keys' in kwargs:
            self.game_keys = kwargs['game_keys']
        else:
            self.game_keys = ['game_total', 'away_team', 'away_total', 'home_team', 'home_total']

        if 'team_names' in kwargs:
            self.team_names = kwargs['team_names']
        else:
            self.team_names = NBATeamNames()

    def _convert_from_utc(self, datestr):
        '''
        http://stackoverflow.com/questions/4770297/python-convert-utc-datetime-string-to-local-datetime
        '''
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = datetime.strptime(datestr, '%Y-%m-%d %H:%M')
        utc = utc.replace(tzinfo=from_zone)
        central = utc.astimezone(to_zone)
        return central

    def _game_code(self, game, date_local):
        return '{0}/{1}{2}'.format(datetime.strftime(date_local, '%Y%m%d'), game['away_team'], game['home_team'])

    def _implied_total(self, game_total, spread):
        '''
        Takes game total and spread and returns implied total based on those values
        '''
        return (game_total/float(2)) - (spread/float(2))

    def _multikeysort(self, items, columns):
        '''
        from https://wiki.python.org/moin/SortingListsOfDictionaries
        '''
        comparers = [ ((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1)) for col in columns]

        def comparer(left, right):
            for fn, mult in comparers:
                result = cmp(fn(left), fn(right))
                if result:
                    return mult * result
            else:
                return 0

        return sorted(items, cmp=comparer)

    def _parse_event(self, event):
        '''
        Handles the heavy lifting parsing each event node
        '''

        game = {}

        # game information
        date_gmt = event.find('event_datetimegmt').get_text()
        if date_gmt:
            game['date_gmt'] = date_gmt
            date_local = self._convert_from_utc(date_gmt)
            game['date_local'] = datetime.strftime(date_local, '%Y-%m-%d')
            game['display_date'] = datetime.strftime(date_local, '%m-%d %H:%M')
            game['start'] = datetime.strftime(date_local, '%H:%M')

        gamenumber = event.find('gamenumber').get_text()

        if gamenumber:
            game['gamenumber'] = gamenumber

        # teams, use long_to_short to get 3 letter team codes
        away, home = event.findAll('participant')
        if away and home:
            game['away_team'] = away.find('participant_name').get_text()
            short_name = self.team_names.long_to_short(game['away_team'])

            if short_name:
                game['away_team'] = short_name

            game['home_team'] = home.find('participant_name').get_text()
            game['home_team_number'] = home.find('rotnum').get_text()
            short_name = self.team_names.long_to_short(game['home_team'])

            if short_name:
                game['home_team'] = short_name

            game['nbacom_gamecode'] = self._game_code(game, date_local)

        # o/u and point spread are found in the period node
        # contains spread and total nodes
        period = event.find('period')

        if period:
            logging.debug('found period for {0}'.format(game.get('nbacom_gamecode', '<missing>')))
            spread = period.find('spread')

            if spread:
                logging.debug('found spread for {0}'.format(game.get('nbacom_gamecode', '<missing>')))
                game['spread_away'] = spread.find('spread_visiting').get_text()
                game['spread_home'] = spread.find('spread_home').get_text()
                logging.debug('spread away, home: {0}, {1}' \
                              .format(game.get('spread_away', '<missing>'),game.get('spread_home', '<missing>')))

                # totals, including calculated implied totals
                total = period.find('total')

                if total:
                    logging.debug('found total for {0}'.format(game.get('nbacom_gamecode', '<missing>')))
                    game_total = total.find('total_points').get_text()

                    if game_total:
                        logging.debug('found game_total for {0}'.format(game.get('nbacom_gamecode', '<missing>')))
                        game['game_total'] = game_total
                        game['home_total'] = self._implied_total(float(game_total), float(game['spread_home']))
                        game['away_total'] = self._implied_total(float(game_total), float(game['spread_away']))
                        logging.debug('away, home: {0}, {1}'.format \
                           (game.get('away_total', '<missing>'), game.get('home_total', '<missing>')))

        else:
            logging.debug('did not find period')

        return game

    def _sort_games(self, games, games_no_totals):
        '''
        Splits games into those with totals and no totals
        Sorts list of dictionaries descending on game_total, then adds games with no totals to list
        '''

        games = self._multikeysort(games, ['-game_total'])
        #logging.debug('games with totals: {0}'.format(pprint.pformat(games)))

        if games_no_totals:
            #logging.debug('games no totals: {0}'.format(pprint.pformat(games_no_totals)))
            games += games_no_totals

        #logging.debug('all games: {0}'.format(pprint.pformat(games)))
        return games

    def odds(self, xml, game_date_cst):
        '''
        Takes xml in, returns sorted and filtered list of game dictionaries:
        game_date_cst in YYYY-MM-DD format
        '''

        # TODO:
            # need to filter based on <league>NBA</league> and <league>Live NBA</league>
        
        games = []
        games_no_totals = []

        # get the list of events
        soup = BeautifulSoup(xml)
        events = soup.findAll('event')
        logging.debug('there are {0} events'.format(len(events)))

        # last item is unwanted - All NFL Games Will Have Second Half Wagering
        for event in events[:-1]:
            game = self._parse_event(event)
            logging.debug(pprint.pformat(game))
            date_local = game.get('date_local', None)

            # filter if specify game date
            if game_date_cst:

                if date_local == game_date_cst:
                    game_total = game.get('game_total', None)

                    if game_total:
                        games.append(game)

                    else:
                        games_no_totals.append(game)

            else:
                game_total = game.get('game_total', None)

                if game_total:
                    games.append(game)

                else:
                    games_no_totals.append(game)

        # sort results and then return
        return self._sort_games(games, games_no_totals)

    def to_csv (self, games, datestr):
        '''
        Takes list of game dictionaries, outputs csv
        '''

        lines = []
        headers = ['date'] + self.game_keys
        lines.append(', '.join(headers))

        for game in games:
            values = [datestr] + [str(game.get(gk, None)) for gk in self.game_keys]
            lines.append(', '.join(values))

        return '\n'.join(lines)

    def to_fw (self, games, datestr):
        '''
        Takes list of game dictionaries, outputs fixed-width table
        '''

        lines = []
        headers = ['date'] + self.game_keys
        formatstr = ' '.join(['{:12s}'] * len(headers))       
        lines.append(formatstr.format(*headers))

        for game in games:
            values = [datestr] + [str(game.get(gk, None)) for gk in self.game_keys]
            formatstr = ' '.join(['{:12s}'] * len(values))       
            lines.append(formatstr.format(*values))

        return '\n'.join(lines)

    def to_tsv (self, games, datestr):
        '''
        Takes list of game dictionaries, outputs csv
        '''

        lines = []
        headers = ['date'] + self.game_keys
        lines.append('\t'.join(headers))

        for game in games:
            values = [datestr] + [str(game.get(gk, None)) for gk in self.game_keys]
            lines.append('\t'.join(values))

        return '\n'.join(lines)

if __name__ == '__main__':
    pass
