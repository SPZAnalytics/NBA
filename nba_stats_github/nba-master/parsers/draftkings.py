import logging
import re

class DraftKingsNBAParser():
    '''
    Contest entries
    Draftkings salaries
    '''

    def __init__(self):
        logging.getLogger(__name__).addHandler(logging.NullHandler())


    def _contest_entry(self, line, contest_id):
        '''
        Takes a line from draft kings contest results file and creates entry dictionary

        Arguments:
            line(str): one row of contest entries
            contest_id(str): unique contest identifier
        
        Returns:
            entry(dict): key-value pair of entry info, such as contest_id, entry_id, player_name, lineup
        '''

        entry = {'contest_id': contest_id}

        fields = [x.strip() for x in line.split(',')]

        try:
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

            if len(lineup) > 0:
                for key, value in list(lineup.items()):
                    entry[key] = value

            return entry

        except:
            logging.exception('error: contest entry {0}'.format(line))

    def _contest_lineup(self, lineup_string):
        '''
        Draft Kings result file provides lineup as one field, PG PG_Name SG SG_Name . . .
        
        Arguments:
            lineup_string(str): PG PG_Name SG SG_Name . . .
        
        Returns:
            lineup(dict): key is position, value is player name
        '''

        lineup = {}

        # PG Patrick Beverley SG Kobe Bryant SF Kent Bazemore PF DeMarcus Cousins C Al Horford F Brandon Bass G D'Angelo Russell UTIL Pau Gasol

        parts = [p.strip() for p in lineup_string.split(' ')]

        if len(parts) == 24:
            lineup['pg'] = ' '.join([parts[1], parts[2]])
            lineup['sg'] = ' '.join([parts[4], parts[5]])
            lineup['sf'] = ' '.join([parts[7], parts[8]])
            lineup['pf'] = ' '.join([parts[10], parts[11]])
            lineup['c'] = ' '.join([parts[13], parts[14]])
            lineup['f'] = ' '.join([parts[16], parts[17]])
            lineup['g'] = ' '.join([parts[19], parts[20]])
            lineup['util'] = ' '.join([parts[22], parts[23]])

        '''       
        pattern = re.compile(r'PG\s+(?P<pg>.*?)\s+SG\s+(?P<sg>.*?)\s+SF\s+(?P<sf>.*?)\s+PF\s+(?P<pf>.*?)\s+C\s+(?P<c>.*?)\s+F\s+(?P<f>.*?)\s+G\s+(?P<g>.*?)\s+UTIL\s+ (?P<util>.*?)')

        match = re.search(pattern, lineup_string)
        if match:
            lineup = {k:v.replace("'", "").strip() for k,v in match.groupdict().items()}

            # can't seem to get last part of regex to work
            # take last item in split string, which is dst
            if 'dst' in lineup and lineup['dst'] == '':
                parts = lineup_string.split(' ')
                lineup['dst'] = parts[-1]
                parts = lineup_string.split(' ')
                lineup['dst'] = parts[-1]
         
        else:
            logging.debug('missing lineup_string')
        '''

        return lineup

    def contest_lineups(self, contest_id, fh):
        '''
        Takes list of lines from Draft Kings result file, returns entry dictionary
        
        Arguments:
            param lines(list): full contest entry line
        
        Returns:
            entries(list): List of contest entry dictionaries
        '''
        
        entries = []

        if isinstance(fh, list):
            for line in fh:
                if 'EntryName' in line:
                    pass

                elif line == '\n':
                    pass

                else:
                    entry = self._contest_entry(contest_id=contest_id, line=line)
                    entries.append(entry)

        else:
            for line in iter(fh.readline, ""):
                if 'EntryName' in line:
                    pass

                elif line == '\n':
                    pass

                else:
                    entry = self._contest_entry(contest_id=contest_id, line=line)
                    entries.append(entry)

            fh.close()
               
        return entries

if __name__ == '__main__':
    pass
