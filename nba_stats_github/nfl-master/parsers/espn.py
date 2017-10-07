# -*- coding: utf-8 -*-
import datetime
import logging
import re

from bs4 import BeautifulSoup

from nfl.teams import nickname_to_code

class ESPNNFLParser(object):

    def __init__(self, **kwargs):

        if 'logger' in kwargs:
            self.logger = kwargs['logger']
        else:
            self.logger = logging.getLogger(__name__) \
                .addHandler(logging.NullHandler())

    def _parse_projections_row(self, row):
        '''
        Parses <tr> element into key-value pairs
        :param row(str): html <tr> element
        :return player(dict):
        '''
        player = {}

        # get the player name / id
        link = row.find("a", {"class": "flexpop"})
        player['espn_id'] = link.get('playerid')
        player['full_name'] = link.string

        # get the player position / team (, Phi WR)
        pos_tm_string = link.nextSibling.string
        pos_tm_string = re.sub(r'\s?,\s+', '', pos_tm_string).strip()
        logging.debug('position team string is %s', pos_tm_string)

        if 'D/ST' in pos_tm_string:
            player['position'] = 'DST'
            player['team'] = self._fix_team_code(link.string.split()[0])
            player['full_name'] = '{0}_DST'.format(player['team'])
            player['injury'] = False

        else:
            try:
                if '*' in pos_tm_string:
                    player['injury'] = True
                    pos_tm_string = player['full_name'].replace('*', '')

                else:
                    player['injury'] = False

                player_team, player_position = pos_tm_string.split()
                player['team'] = re.sub(r'\s+', '', player_team)
                player['position'] = re.sub(r'\s+', '', player_position)

            except ValueError:
                self.logger.exception("pos_tm_string error")

        # now get the projected points
        fantasy_points = row.find("td", {"class": "appliedPoints"}).string
        if '--' in fantasy_points:
            player['fantasy_points'] = 0
        else:
            player['fantasy_points'] = fantasy_points

        return player

    def projections(self, content):
        '''
        Takes HTML, returns list of player dictionaries
        :param content: html page of projections
        :return rows(list): player dictionaries
        '''

        rows = []
        soup = BeautifulSoup(content)

        for row in soup.findAll("tr", {"class": "pncPlayerRow"}):
            player = self._parse_projections_row(row)
            rows.append(player)

        return rows

    def _ww_player_cell(self, cell):
        '''
        [u'Buccaneers D/ST D/ST']
        [u'Dexter McCluster', u'Ten RB']
        [u'Brandon LaFell', u'Cin WR']
        [u'Kenny Stills', u'Mia WR  Q']
        '''
        player = {}
        ptp = cell.text
        a = cell.find('a')
        if a:
            player['espn_id'] = a['playerid']
            player['season'] = a['seasonid']
            player['espn_player_name'] = a.text.strip()

        # [u'Buccaneers D/ST D/ST']
        if 'D/ST' in ptp:
            pattern = r'(.*?)\s+D/ST'
            match = re.match(pattern, ptp)
            if match:
                player['espn_player_name'] = '{} Defense'.format(match.group(1))
                player['player_position'] = 'DST'
                player['player_team'] = nickname_to_code(match.group(1))
                # need to add team code from Falcons, Seahawks, etc.

        # [u'Kenny Stills', u'Mia WR  Q']
        elif '  ' in ptp:
            pattern = r'(.*?),\s+(\w{2,4})\s+(\w{2})\s+(\w+)'
            match = re.match(pattern, ptp)
            if match:
                if not player.get('espn_player_name'): player['espn_player_name'] = match.group(1)
                player['player_team'] = match.group(2).upper()
                player['player_position'] = match.group(3)
                player['player_inj'] = match.group(4)

        # [u'Dexter McCluster', u'Ten RB']
        else:
            # do generic split routine
            pn, tp = ptp.split(', ')
            if not player.get('espn_player_name'): player['espn_player_name'] = pn
            player['player_team'], player['player_position'] = tp.split()

        return player

    def league_rosters(self, rosters):
        '''

        Args:
            rosters (dict): key is person_teamid, value is html string

        Returns:
            rosters (list): list of dict
                            keys --
        '''
        rosters = []

        for t, c in rosters.items():

            rosters += self.team_roster(t, c)
        return rosters

    def lovehate(self, season, week, lh):
        '''

        Args:
            season(int):
            week(int):
            d(dict): keys are position_love, position_hate

        Returns:
            players(list): of player dict
        '''

        players = []

        for poslh, ratings in lh.items():
            pos = poslh.split('_')[0]
            label = ratings.get('label')
            sublabel = None

            if label in ('favorite', 'bargain', 'desparate'):
                sublabel = label
                label = 'love'
            for link in ratings.get('links'):
                url = link.split('"')[1]
                site_player_id, site_player_stub = url.split('/')[7:9]
                site_player_name = link.split('>')[1].split('<')[0]

        print season, week, pos, label, sublabel, site_player_id, site_player_stub, site_player_name


    def team_roster(self, team_string, content):
        '''
        Parses one team clubhouse
        Args:
            team_string (str): TEAMOWNER_TEAMID
            content (str): html string

        Returns:
            roster (list): of player dict
        '''

        roster = []
        team_owner, team_id = team_string.split('_')

        soup = BeautifulSoup(content, 'lxml')
        t = soup.find('table', {'id': 'playertable_0'})
        if not t: return roster
        today = datetime.datetime.strftime(datetime.date.today(), '%m-%d-%Y')

        for tr in t.findAll('tr', {'class': 'pncPlayerRow'}):
            player = {}
            pid = tr.get('id')
            if pid: player['espn_player_id'] = re.findall(r'\d+', pid)[0]
            slot = tr.find('td', {'class': 'playerSlot'})
            if slot: player['slot'] = slot.text.strip()
            player_name = tr.find('a', {'class': 'flexpop'})
            if player_name: player['espn_player_name'] = player_name.text.strip()
            player['fantasy_team'] = team_owner
            player['fantasy_team_id'] = team_id
            player['roster_date'] = today
            if player.get('espn_player_name', None):
                roster.append(player)

        return roster

    def waiver_wire(self, content):
        '''

        Args:
            content (str): HTML string from espn waiver wire page

        Returns:
            players (list): list of player dict
                {'espn_id': '11373',
                'espn_player_name': u'Jacob Tamme',
                'player_position': u'TE',
                'player_team': u'Atl',
                'season': '2016'}

        Usage:
            from nfl.scrapers.espn import ESPNNFLScraper as ES
            from nfl.parsers.espn import ESPNNFLParser as EP
            s = ES()
            p = EP()
            content = s.waiver_wire()
            players = p.waiver_wire(content)
        '''

        players = []

        # irregular use of non-breaking spaces; easier to remove at start
        content = content.replace('&nbsp;', ' ')
        content = content.replace('*', ' ')

        soup = BeautifulSoup(content, 'lxml')
        t = soup.find('table', {'id': 'playertable_0'})

        #loop through rows in table
        for tr in t.findAll('tr', {'class': 'pncPlayerRow'}):
            tds = tr.findAll('td')
            if not tds or len(tds) == 0: next
            player = self._ww_player_cell(tds[0])
            players.append(player)
            
        return players

if __name__ == "__main__":
    pass
    #p = ESPNNFLParser()
    #with open('/home/sansbacon/workspace/nfl/parsers/clubhouse.html', 'r') as infile:
    #    pprint.pprint(p.team_roster('Fred_7', infile.read()))