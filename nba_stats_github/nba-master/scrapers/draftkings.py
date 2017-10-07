import mmap
import os

from nba.scrapers.scraper import BasketballScraper

class DraftKingsNBAScraper(BasketballScraper):
    '''

    Examples:
        s = DraftKingsNBAScraper()
        s.contest_fn = (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'results.csv'))
        mm = s.contest_data(s.contest_fn)
        while True:
            line=mm.readline()
            if line == '': break
            print line.strip()
    '''

    def contest_data(self, fname):
        '''
        Uses memory map instead of file_io due to filesize

        Arguments:
            fname(str): .csv file with draft kings contest results
        
        Returns:
            mm(mmap): memory map of file
        '''

        if os.path.exists(fname):

            with open(fname, 'r+b') as f:
                return mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)

        else:
            raise ValueError('contest_data(fname): fname must exist')

    def salary_data(self, fname):

        if os.path.exists(fname):
            with open(fname, 'r') as f:
                return f.readlines()

        else:
            raise ValueError('salary_data(fname): fname must exist')

if __name__ == '__main__':
    pass
