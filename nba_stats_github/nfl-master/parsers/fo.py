# -*- coding: utf-8 -*-
import logging
import re

from bs4 import BeautifulSoup


class FootballOutsidersNFLParser(object):
    '''

    '''

    def dl(self, content, season, week):
        # there can be 2 teams listed on one row b/c pass and rush usually not the same team

        rush_headers = ['rush_rank', 'team', 'adj_line_yards', 'rb_yards', 'power_success', 'power_rank', 'stuffed',
                        'stuffed_rank', 'sec_level_yards', 'sec_level_rank', 'open_field_yards', 'open_field_rank']
        pass_headers = ['team', 'pass_rank', 'sacks', 'adj_sack_rate']

        soup = BeautifulSoup(content)
        t = soup.find('table', {'class': 'stats'})
        teams = {}

        # skip first two lines - double headers
        for tr in t.find_all('tr')[2:]:
            tds = tr.find_all('td')
            if len(tds) != len(rush_headers) + len(pass_headers):
                continue

            # rushing
            rvals = [str(td.string).replace('%', '').strip() for td in tds[0:12]]
            team = rvals[1]
            if teams.has_key(team):
                for idx, h in enumerate(rush_headers):
                    if h == 'team':
                        continue
                    else:
                        teams[team][h] = rvals[idx]
            else:
                teams[team] = dict(zip(rush_headers, rvals))

            # passing
            pvals = [str(td.string).replace('%', '').strip() for td in tds[12:]]
            team = pvals[0]
            if teams.has_key(team):
                for idx, h in enumerate(pass_headers):
                    if h == 'team':
                        continue
                    else:
                        teams[team][h] = pvals[idx]
            else:
                teams[team] = dict(zip(pass_headers, pvals))

            teams[team]['season_year'] = season
            teams[team]['week'] = week

        return teams.values()

    def snap_counts(self, content, season, week):
        players = []
        headers = ['player', 'team', 'position', 'started', 'total_snaps', 'off_snaps', 'off_snap_pct', 'def_snaps', 'def_snap_pct', 'st_snaps', 'st_snap_pct']
        soup = BeautifulSoup(content, 'lxml')
        t = soup.find('table', {'id': 'dataTable'})
        tb = t.find('tbody')

        for row in tb.find_all('tr'):
            cells = [td.text.strip() for td in row.find_all('td')]
            player = dict(zip(headers, cells))
            player['season'] =  season
            player['week'] = week
            players.append(player)

        return players

if __name__ == "__main__":
    pass