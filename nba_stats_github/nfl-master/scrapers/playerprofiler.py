'''
PlayerProfilerNFLScraper
For use by subscribers
Non-subscribers should be aware of site's TOS
'''

import logging

from ewt.scraper import EWTScraper


class PlayerProfilerNFLScraper(EWTScraper):
    '''
    Usage:
        s = PlayerProfilerNFLScraper()

    '''

    def __init__(self, **kwargs):
        # see http://stackoverflow.com/questions/8134444
        EWTScraper.__init__(self, **kwargs)
        logging.getLogger(__name__).addHandler(logging.NullHandler())

        if 'polite' in 'kwargs':
            self.polite = kwargs['polite']
        else:
            self.polite = True

    def player_page(self, site_player_id):
        '''
        Gets single player page from playerprofiler
        '''
        url = 'https://www.playerprofiler.com/wp-admin/admin-ajax.php?action=playerprofiler_api&endpoint=%2Fplayer%2F{site_player_id}'
        return self.get(url.format(site_player_id=site_player_id))

    def players(self):
        '''
        Gets list of players, with ids, from playerprofiler
        '''
        url = 'https://www.playerprofiler.com/wp-admin/admin-ajax.php?action=playerprofiler_api&endpoint=%2Fplayers'
        return self.get(url)

    def rankings(self):
        '''
        Gets current season, dynasty, and weekly rankings from playerprofiler
        '''
        url = 'https://www.playerprofiler.com/wp-admin/admin-ajax.php?action=playerprofiler_api&endpoint=%2Fplayer-rankings'
        return self.get(url)

if __name__ == "__main__":
    pass