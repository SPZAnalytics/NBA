    def _average_adp(self, values):
        '''
        Takes list of values, returns average after dropping high/lows if 4 or more, just average otherwise
        :param values (list):
        :return average (float):
        '''

        if len(values) < 4:
            return sum(values) / float(len(values))

        else:
            values.sort()
            trimmed = values[1:-1]
            return sum(trimmed) / float(len(trimmed))


    def _headers_from_csv(self, header_trigger, content=None, fname=None):
        '''
        Parses csv content or file and returns header row and line number of header row
        :param header_trigger (str): something that appears in header line that identifies it
        :param content: fetch .csv from web
        :param fname: fetch .csv from file
        :return: headers (list): List of headers from .csv file
        '''

        # the csv file has a number of lines to skip before header line
        n = 0
        if content:
            for line in content.splitlines():
                n += 1

                if header_trigger in line:
                    headers = [x.strip() for x in line.split('\t') if x is not None and x is not ""]
                    break
        elif fname:
            # first time around just skipping irrelevant lines, going to header lines
            # save value of 'n' for reading later on
            with open(fname, "rU") as f:
                for line in f.readlines():
                    n += 1

                    if header_trigger in line:
                        headers = [x.strip() for x in line.split('\t') if x is not None and not x == '']
                        break

                f.close()
        else:
            raise ValueError('must pass content or fname')

        return headers, n

    def _parse_adp_row(self, row):
        '''
        Private method converts row to dictionary, calculates average ADP
        :param row: from csv.dictreader
        :return player(dictionary: row parsed into dictionary + calculated field
        '''

        player = {}
        values = []

        for k in row.keys():
            value = row.get(k, None)

            if value is not None and re.match(r'\d+', value):
                try:
                    player[k] = float(value)
                    values.append(player[k])
                except:
                    player[k] = value
                    logging.debug('key is %s, value is %s of type %s' % (k, player[k], type(player[k])))

            elif value is not None and not value == '':
                player[k] = value

        if len(values) < 4:
            player['average_adp'] = sum(values) / float(len(values))

        else:
            values.sort()
            trimmed = values[1:-1]
            player['average_adp'] = sum(trimmed) / float(len(trimmed))

        return player

    def adp(self, content=None, fname=None):
        '''
        Parses csv and returns list of player dictionaries
        Args:
            content (str): csv typically fetched by FantasyProsNFLScraper class
            fname (str): path to local csv file
        Returns:
            List of dictionaries if successful, empty list otherwise.
        '''

        players = []
        header_trigger='ESPN'

        if content:
            headers, n = self._headers_from_csv(header_trigger=header_trigger, content=content)
            headers = self.fix_headers(headers)
            lines = islice(content.splitlines(), n, None)

            reader = csv.DictReader(lines, fieldnames=headers, dialect=csv.excel_tab)
            for row in reader:
                player = self._parse_adp_row(row)
                players.append(player)

        elif fname:
            # the csv file has a number of lines to skip before header line
            # will open and read the file twice, 2nd time around take slice starting after header line

                # use fix_headers to try to standardize across sites (although not perfect)
                headers, n = self._headers_from_csv(fname=fname, header_trigger='ESPN')
                headers = self.fix_headers(headers)
                f = islice(open(fname, "rU"), n, None)
                reader = csv.DictReader(f, fieldnames=headers, dialect=csv.excel_tab)

                for row in reader:
                    player = self._parse_adp_row(row)
                    players.append(player)

        else:
            raise ValueError('must pass content or fname parameter')

        return players

    def fix_header(self, header):
        '''
        Looks at global list of headers, can provide extras locally
        :param headers:
        :return:
        '''

        fixed = {
            'Rank': 'overall_rank',
            'Player Name': 'full_name',
            'Position': 'position',
            'Team': 'team',
            'Bye Week': 'bye',
            'Best Rank': 'best_rank',
            'Worst Rank': 'worst_rank',
            'Worst Rank': 'worst_rank',
            'Avg Rank': 'average_rank',
            'Std Dev': 'stdev_rank',
            'ADP': 'adp'
        }

        # TODO: normal pattern was not working
        #return fixed.get(header, header)
        fixed_header = self._fix_header(header)
        logging.debug('parser._fix_header fixed header')
        logging.debug(fixed_header)

        # fixed_header none if not found, so use local list
        if not fixed_header:
            return fixed.get(header, header)

        else:
            return fixed_header

    def fix_headers(self, headers):
        return [self.fix_header(header) for header in headers]

    def _player_page(self,content, pos):
        '''
        Parses page of fantasypros players

        Args:
            content(str):

        Returns:
            players(list): of player dict, keys: pos, site, site_player_id, site_player_name
        '''

        players = []
        soup = BeautifulSoup(content, 'lxml')
        t = soup.find('table', {'id': 'data'})
        tbody = t.find('tbody')
        pattern = re.compile(r'mpb-player-(\d+)')

        for tr in tbody.findAll('tr', {'class': pattern}):
            p = {'site': 'fantasypros', 'pos': pos}

            sm = tr.find('small', {'class': 'grey'})
            if sm:
                p['team'] = sm.text

            a = tr.find('a', {'href': re.compile(r'/nfl/players')})
            try:
                match = re.match(pattern, tr['class'][0])
                if match:
                    p['site_player_id'] = match.group(1)
                    p['site_player_name'] = a.text
                    players.append(p)

            except Exception as e:
                logging.exception(e)

        return players

    def players(self, dir):
        '''
        Arguments:
            dir(str): directory where HTML files located

        Returns:
            players (list): dict with player_id from nfl.players

        Usage:
            p = FantasyProsNFLParser()
            players = p.players('/home/sansbacon/fpros')
            with open('fpros-players.json', 'w') as outfile:
                json.dump(players, outfile)
        '''
        players = []
        base_fname = os.path.join(dir, '{}.html')
        for pos in ['QB', 'RB', 'TE', 'WR']:
            fname = base_fname.format(pos.lower())
            if os.path.exists(fname):
                with open(fname, 'r') as infile:
                    players += self._player_page(infile.read(), pos)

        return players

    
    def _parse_projections_rows(self, reader):

        players = []

        for row in reader:

            row = {k: v for k, v in row.items() if k and v}

            # fantasypros lists position as RB1, QB2, so need to strip numbers
            row['position'] = ''.join(i for i in row['position'] if not i.isdigit())

            # standardize names for lookup
            full_name, first_last = NameMatcher.fix_name(row['full_name'])
            row['full_name'] = full_name
            row['first_last'] = first_last
            players.append(row)

        return players


    def projections (self, content=None, fname=None):

        header_trigger = 'ADP'

        if content:

            # the csv file has a number of lines to skip before header line
            headers, n = self._headers_from_csv(content=content, header_trigger=header_trigger)
            headers = self.fix_headers(headers)
            lines = islice(content.splitlines(), n, None)
            reader = csv.DictReader(lines, fieldnames=headers, dialect=csv.excel_tab)
            players = self._parse_projections_rows(reader)            

        elif fname:

            # the csv file has a number of lines (n) to skip before header line
            headers, n = self._headers_from_csv(fname=fname, header_trigger=header_trigger)
            headers = self.fix_headers(headers)
            lines = islice(content.splitlines(), n, None)
            reader = csv.DictReader(lines, fieldnames=headers, dialect=csv.excel_tab)
            players = self._parse_projections_rows(reader)

        else:
            raise ValueError('must pass content or fname parameter')

        return players
    '''
