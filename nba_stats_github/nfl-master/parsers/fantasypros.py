# -*- coding: utf-8 -*-
import logging
import re

from bs4 import BeautifulSoup

class FantasyProsNFLParser(object):
    '''
    used to parse Fantasy Pros projections and ADP pages
    '''

    def __init__(self,**kwargs):

        if 'logger' in kwargs:
          self.logger = kwargs['logger']
        else:
          self.logger = logging.getLogger(__name__)

    def _wr_flex(self, t, season, week, position='flex'):
        '''
        Different table structure for flex vs. positional rankings
        Args:
            t:
            season:
            week:
            position:

        Returns:
            players(list): of player dict
        '''
        players = []
        headers = ['weekly_rank', 'site_player_id', 'site_player_name', 'team', 'best', 'worst', 'avg', 'stdev']
        for tr in t.findAll('tr'):
            td = tr.find('td')

            # skip these rows without further processing
            if not td: continue
            if td.text and re.match(r'[A-Z]+', td.text): continue

            # rank in td[0]
            td = tr.find('td')
            if td: rank = td.text
            else: rank = None

            # most pages have 2 links, easiest to parse 2nd link that has no text
            a = tr.find('a', class_ = 'fp-player-link')
            if a and a.has_attr('fp-player-name'): site_player_name = a['fp-player-name']
            else: site_player_name = None
            if a and a.has_attr('class'):site_player_id = a['class'][-1].split('-')[-1]
            else: site_player_id = None

            if not site_player_name:
                a = tr.find('a')
                if a: site_player_name = a.text

            # player team wrapped in <small> element
            if tr.find('small'):
                match = re.match(r'\(([A-Z]+)\)', tr.find('small').text)
                if match:
                    team = match.group(1)
                else:
                    team = tr.find('small').text
                    if team: team = team.strip().split(' ')[0].replace('(', '').replace(')', '')

            # need best, worst, ave, std tds[2:]
            tds = tr.findAll('td', {'class': re.compile(r'tier')})
            if tds:
                summ = [td.text.strip() for td in tds]
            else:
                summ = [td.text.strip() for td in tr.findAll('td')[3:]]

            # zip up and add
            player = dict(zip(headers, [rank, site_player_id, site_player_name, team] + summ))
            player['season'] = season
            player['week'] = week
            player['pos'] = position
            player['site'] = 'fantasypros'
            players.append(player)

        return players

    def _wr_no_flex(self, t, season, week, position):
        '''
        Different table structure for flex vs. positional rankings
        Args:
            t:
            season:
            week:
            position:

        Returns:
            players(list): of player dict

        '''
        players = []

    def weekly_rankings(self, content, season, week, position):
        players = []
        content = content.replace("\xc2\xa0", "")
        soup = BeautifulSoup(content, 'lxml')
        t = soup.find('table', id='data')
        headers = ['weekly_rank', 'site_player_id', 'site_player_name', 'team', 'best', 'worst', 'avg', 'stdev']
        for tr in t.findAll('tr'):
            td = tr.find('td')

            # skip these rows without further processing
            if not td: continue
            if td.text and re.match(r'[A-Z]+', td.text): continue

            # rank in td[0]
            td = tr.find('td')
            if td: rank = td.text
            else: rank = None

            # most pages have 2 links, easiest to parse 2nd link that has no text
            a = tr.find('a', class_ = 'fp-player-link')
            if a and a.has_attr('fp-player-name'): site_player_name = a['fp-player-name']
            else: site_player_name = None
            if a and a.has_attr('class'):site_player_id = a['class'][-1].split('-')[-1]
            else: site_player_id = None

            if not site_player_name:
                a = tr.find('a')
                if a: site_player_name = a.text

            # player team wrapped in <small> element
            if tr.find('small'):
                match = re.match(r'\(([A-Z]+)\)', tr.find('small').text)
                if match:
                    team = match.group(1)
                else:
                    team = tr.find('small').text
                    if team: team = team.strip().split(' ')[0].replace('(', '').replace(')', '')

            # need best, worst, ave, std tds[2:]
            tds = tr.findAll('td', {'class': re.compile(r'tier')})
            if tds:
                summ = [td.text.strip() for td in tds]
            else:
                summ = [td.text.strip() for td in tr.findAll('td')[3:]]

            # zip up and add
            player = dict(zip(headers, [rank, site_player_id, site_player_name, team] + summ))
            player['season'] = season
            player['week'] = week
            player['pos'] = position
            player['site'] = 'fantasypros'
            players.append(player)

        return players

    def weekly_rankings(self, content, season, week, position):
        '''
        TODO: need to write parsing routine for flex rankings page
        TODO: need to adjust for standard, half-ppr, and ppr
              add column to weekly_rankings table and adjust the unique constratint accordingly
        Args:
            content:
            season:
            week:
            position:

        Returns:

        '''

        content = content.replace("\xc2\xa0", "")
        soup = BeautifulSoup(content, 'lxml')
        t = soup.find('table', id='data')

        if position == 'flex':
            return self._wr_flex(t, season, week)
        else:
            return self._wr_no_flex(t, season, week, position)

    '''
        def weekly_rankings_html(content):
            players = []
            soup = BeautifulSoup(content, 'lxml')
            t = soup.find('table', id='data')
            headers = ['rank', 'site_player_id', 'site_player_name', 'team', 'best', 'worst', 'ave', 'stdev']
            for tr in t.findAll('tr'):
                vals = []
                td = tr.find('td')
                if not td:
                    next
                elif td.text and re.match(r'[A-Z]+', td.text):
                    next
                else:
                    tds = tr.findAll('td')
                    rank = tds[0].text
                    a = tr.find('a')
                    if a:
                        cl = a.get('class', None)
                        if cl:
                            site_player_id = a['class'].split('-')[-1]
                        else:
                            site_player_id = None
                        ppn = a.get('pf-player-name', None)
                        if ppn:
                            site_player_name = ppn
                        else:
                            site_player_name = a.text
                        matchup = tr.find('small')
                        if matchup:
                            match = re.match(r'\(([A-Z]+)\)', matchup.text)
                            if match:
                                team = match.group(1)
                            else:
                                team = matchup.text.strip().split(' ')[0].replace('(', '').replace(')', '')
                        else:
                            team = matchup.text

                        print(rank, site_player_id, site_player_name, team)

    '''

if __name__ == "__main__":
    pass
