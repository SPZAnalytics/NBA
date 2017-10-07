imoprt logging
import mmap
import os

import pandas as pd


class DraftKingsNFLScraper:
    '''
    s = DraftKingsNFLScraper()
    s.contest_fn = (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sample.csv'))
    mm = s.contest_data(s.contest_fn)
    while True:
        line=mm.readline()
        if line == '': break
        print line.strip()
    '''

    def __init__(self):
        self._contest_fn = None

    @property
    def contest_fn(self):
        return self._contest_fn

    @contest_fn.setter
    def contest_fn(self, x):
        self._contest_fn = x

    def contest_data(self, fname):
        '''
        Uses memory map instead of file_io due to filesize
        :param fname(str): .csv file with draft kings contest results
        :return mm(mmap): memory map of file
        '''
        try:
            with open(fname, 'r+b') as f:
                return mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)

        except Exception as e:
            logging.exception(e)

    def _entry(self, line, contest_id):

        entry = {'contest_id': contest_id}
        
        fields = [x.strip() for x in line.split(',')]
        
        entry['contest_rank'] = fields[0]
        entry['entry_id'] = fields[1]

        # entries is in format: ScreenName (entryNumber/NumEntries)
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
        lineup = get_lineup(lineup_string)
        for position in lineup:
            entry[position] = lineup[position]

        return entry
        
    def _lineup(self, lineup_string):

        lineup = {}
        pattern = re.compile(r'QB\s+(?P<qb>.*?)\s+RB\s+(?P<rb1>.*?)\s+RB\s+(?P<rb2>.*?)\s+WR\s+(?P<wr1>.*?)\s+WR\s+(?P<wr2>.*?)\s+WR\s+(?P<wr3>.*?)\s+TE\s+(?P<te>.*?)\s+FLEX (?P<flex>.*?) DST(?P<dst>.*?)')

        if ',' in line:
            fields = [x.strip() for x in line.split(',')]
            lineup_string = fields[-1]

            match = re.search(pattern, lineup_string)
            if match:
                lineup = match.groupdict()
                
                # can't seem to get last part of regex to work
                if 'dst' in lineup and lineup['dst'] == '':
                    parts = lineup_string.split(' ')
                    lineup['dst'] = parts[-1]
                    parts = lineup_string.split(' ')
                    lineup['dst'] = parts[-1]

            else:
                root.debug('missing lineup_string')
                
        return lineup

    def salary_data(self, fname):

        try:
            df = pd.read_csv(fname, header=True)
        except:
            logging.exception('salary_data(fname): fname must exist')

if __name__ == '__main__':
    pass
