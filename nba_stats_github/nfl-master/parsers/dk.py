import datetime
import json
import logging
import re

from bs4 import BeautifulSoup


class DraftKingsNFLParser():
    '''
    Contest entries
    Draftkings lobby
    Draftkings salaries
    '''

    def _contest_entry(self, line, contest_id):
        '''
        Takes a line from draft kings contest results file and creates entry dictionary
        :param line(str):
        :param contest_id(str):
        :return entry(dict):
        '''
        entry = {'contest_id': contest_id}
        fields = [x.strip() for x in line.split(',')]
        entry['contest_rank'] = fields[0]
        entry['entry_id'] = fields[1]

        # entries is in format: ScreenName (entryNumber/NumEntries)
        # if person has 1 entry, then it will not show (1/1)
        if '(' in fields[2]:
            name, entries = [x.strip() for x in fields[2].split(' ')]
            entry['entry_name'] = name
            match = re.search(r'\d+/(\d+)', entries)
            if match:
                entry['num_entries'] = match.group(1)
        else:
            entry['entry_name'] = fields[2]
            entry['num_entries'] = 1

        # fantasy points scored
        entry['points'] = fields[4]

        # parse lineup_string into lineup dictionary, add to entry
        lineup_string = fields[5]
        lineup = self._contest_lineup(lineup_string)
        for key, value in lineup.items():
            entry[key] = value

        return entry

    def _contest_lineup(self, lineup_string):
        '''
        Draft Kings result file provides lineup as one field, QB QB_Name RB RB_Name . . .
        :param lineup_string(str): QB QB_Name RB RB_Name . . .
        :return lineup(dict):
        '''
        lineup = {}
        pattern = re.compile(r'QB\s+(?P<qb>.*?)\s+RB\s+(?P<rb1>.*?)\s+RB\s+(?P<rb2>.*?)\s+WR\s+(?P<wr1>.*?)\s+WR\s+(?P<wr2>.*?)\s+WR\s+(?P<wr3>.*?)\s+TE\s+(?P<te>.*?)\s+FLEX (?P<flex>.*?) DST(?P<dst>.*?)')

        match = re.search(pattern, lineup_string)
        if match:
            lineup = {k:v.strip() for k,v in match.groupdict().items()}

            # can't seem to get last part of regex to work
            # take last item in split string, which is dst
            if 'dst' in lineup and lineup['dst'] == '':
                parts = lineup_string.split(' ')
                lineup['dst'] = parts[-1]
                parts = lineup_string.split(' ')
                lineup['dst'] = parts[-1]
        else:
            logging.debug('missing lineup_string')

        return lineup

    def _contest_lines(self):
        '''
        TODO: move to testfile
        '''
        return ['Rank,EntryId,EntryName,TimeRemaining,Points,Lineup',
                '1,125913309,jetsfanman (3/3),0,238.04,QB Ben Roethlisberger RB Darren Sproles RB Chris Ivory WR Stevie Johnson WR Antonio Brown WR Julio Jones TE Rob Gronkowski FLEX Tyler Eifert DST Jets',
                '2,126600097,kasiki28 (2/2),0,226.94,QB Sam Bradford RB Alfred Morris RB Carlos Hyde WR Julio Jones WR Jordan Matthews WR Davante Adams TE Travis Kelce FLEX Tyler Eifert DST Panthers',
                '3,125805837,doubledouces777 (4/6),0,226.78,QB Carson Palmer RB Darren Sproles RB Chris Ivory WR Stevie Johnson WR Antonio Brown WR Julio Jones TE Rob Gronkowski FLEX Martellus Bennett DST Jets',
                '4,121765199,WashMoBallas (1/7),0,226.34,QB Tony Romo RB Matt Forte RB Chris Ivory WR Julian Edelman WR Antonio Brown WR Kendall Wright TE Tyler Eifert FLEX Stevie Johnson DST Dolphins'
                ]

    def _salary(self, line):
        '''
        Processes single line of salary file
        TODO: see if deprecated in light of pandas solution
        TODO: should call _salary_game_info for additional fields
        '''
        player = {}

        # "Position","Name","Salary","GameInfo","AvgPointsPerGame","teamAbbrev"    
        fields = [x.strip() for x in line.split(',')]
        player['position'] = fields[0].replace('"', '')
        player['full_name'] = fields[1].replace('"', '')
        player['salary'] = fields[2].replace('"', '')
        player['game_info'] = fields[3].replace('"', '')
        player['fantasy_points_per_game'] = fields[4].replace('"', '')
        player['team_code'] = fields[5].replace('"', '')

        return player

    def _salary_game_info(self, game_info, team_code):
        '''
        TODO: see if duplicative, change to is_home (boolean)
        #Atl@NYG 01:00PM ET
        Figures out who opponent is and whether player is home or away 
        Returns site (home or away) and opponent (2 or 3 character team code)
        '''    
        pattern = re.compile(r'(\w+)@(\w+)')    
        match = re.search(pattern, game_info)
        if match:
            away_team = match.group(1)
            home_team = match.group(2)
            
            if away_team == team_code:
                site = 'away'
                opponent = home_team
            elif home_team == team_code:
                site = 'home'
                opponent = away_team           
            else:
                site = None
                opponent = None
                logging.error('away or home team must match team_code')
        else:
            logging.error('could not find home and away team')
    
        return site, opponent

    def contest_lineups(self, contest_id, fh):
        '''
        Takes list of lines from Draft Kings result file, returns entry dictionary
        :param fh(handle): is a handle, such as mmap or open file
        :return entries(list): List of contest entry dictionaries
        '''
        entries = []
        for line in fh:
            if 'EntryName' in line:
                pass
            elif line == '\n':
                pass
            else:
                entry = self._contest_entry(contest_id=contest_id, line=line)
                entries.append(entry)
        return entries

    def dk_lobby(self, content, season, week):
        '''
        Parses dk lobby (json embedded in HTML page) and returns list of contest dicts

        Args:
            content(str): HTML from lobby
            season (int):
            week (int): for football only

        Returns:
            contests(list): of contest dicts

        Usage:
            logging.basicConfig(level=logging.ERROR)
            from nfl.db.nflpg import NFLPostgres
            from nfl.parsers.dk import DraftKingsNFLParser

            dkp = DraftKingsNFLParser()
            nflp = NFLPostgres(database='nfl', user=os.environ['NFLPGUSER'], password=os.environ['NFLPGPASSWORD'])
            dn = os.path.basename(inspect.getfile(DraftKingsNFLParser.__class__))
            with open(os.path.join(dn, 'dklobby.html', 'r') as infile:
                contests = dkp.dk_lobby(infile.read(), 2016, 1)
                nflp.insert_dicts(contests, 'dk_contests')
        '''

        contests = []
        pattern = re.compile(r'packagedContests = (\[.*?\])\;', re.MULTILINE | re.DOTALL)
        match = re.search(pattern, content)

        if match:
            for contest in json.loads(match.group(1)):
                # 1 - NFL, 2- MLB, NBA??
                if contest.get('s') == 1:
                    # convert epoch string to date
                    ds = re.findall('\d+', contest.get('sd', ''))[0]
                    cd = datetime.datetime.strftime(datetime.datetime.fromtimestamp(float(ds) / 1000), '%m-%d-%Y')

                    # create context dict
                    headers = ['season', 'week', 'contest_name', 'contest_date', 'contest_slate', 'contest_fee',
                               'contest_id', 'max_entries', 'contest_size', 'prize_pool']
                    vals = [season, week, contest.get('n'), cd, contest.get('sdstring'), contest.get('a'),
                            contest.get('id'), contest.get('mec'), contest.get('m'), contest.get('po')]
                    contests.append(dict(zip(headers, vals)))

        return contests

    def parallel_contest_entries(self):
        pass
        '''
        # http://stackoverflow.com/questions/4047789/parallel-file-parsing-multiple-cpu-cores
        def worker(lines):
            #Make a dict out of the parsed, supplied lines
            result = {}
            for line in lines.split('\n'):
                k, v = parse(line)
                result[k] = v
            return result

        if __name__ == '__main__':
            # configurable options.  different values may work better.
            numthreads = 8
            numlines = 100

            lines = open('input.txt').readlines()

            # create the process pool
            pool = multiprocessing.Pool(processes=numthreads)

            # map the list of lines into a list of result dicts
            result_list = pool.map(worker,
                                   (lines[line:line + numlines] for line in xrange(0, len(lines), numlines)))

            # reduce the result dicts into a single dict
            result = {}
            map(result.update, result_list)
        '''

    def salaries(dk_players):
        '''
        Returns list of dict to insert in nfl.salaries table
        TODO: move to appropriate component
        
        Args:
            dk_players(list): list of dict from DKSalaries csv file
        '''   
        l = []
        for p in dk_players:
            # cp will be partial copy of player dict
            # fields match what is required for nfl.salaries table
            cp = {}           
            cp['source'] = 'dk'
            cp['source_player_id'] = p['dk_key']
            cp['dfs_site'] = 'dk'
            cp['dfs_site_player_id'] = p['dk_key']
            cp['season'] = 2016
            cp['week'] = 1
            cp['team'] = p['team']
            cp['opp'] = p['opp']
            cp['pos'] = p['Position']
            cp['salary'] = p['Salary']
            cp['is_home'] = p['is_home']
            try:
                parts = p['Name'].split(' ')
                cp['player'] = parts[1].strip() + ', ' + parts[0].strip()
            except:
                cp['player'] = p['Name']
            
            l.append(cp)

        return l

if __name__ == '__main__':
    pass
