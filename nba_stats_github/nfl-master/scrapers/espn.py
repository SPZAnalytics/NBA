'''
ESPNNFLScraper

'''

from ewt.scraper import EWTScraper
import logging


class ESPNNFLScraper(EWTScraper):
    '''

    '''

    def __init__(self, **kwargs):
        # see http://stackoverflow.com/questions/8134444
        EWTScraper.__init__(self, **kwargs)

        if 'logger' in kwargs:
            self.logger = kwargs['logger']
        else:
            self.logger = logging.getLogger(__name__) \
                .addHandler(logging.NullHandler())

        if 'maxindex' in kwargs:
            self.maxindex = kwargs['maxindex']
        else:
            self.maxindex = 400

        if 'projection_urls' in 'kwargs':
            self.projection_urls = kwargs['projection_urls']
        else:
            base_url = 'http://games.espn.go.com/ffl/tools/projections?'
            idx = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360]
            self.projection_urls = ['{}startIndex={}'.format(base_url, x) for x in idx]

    def league_rosters(self, teams=None, league_id=302946, season=2016):
        rosters = {}

        if not teams:
            teams = {
                'Ranjan': 1, 'Allen': 3, 'Gary': 6, 'Fred': 7,
                'Chad': 8, 'Patrick': 9, 'Lu': 11, 'Eric': 12,
                'Jared': 14, 'Sarah': 15, 'Emily': 17, 'Pong': 18,
                'Meredith': 19, 'Paco': 20, 'Michael': 22, 'Jean': 23
            }

        url = 'http://games.espn.com/ffl/clubhouse?leagueId={}&teamId={}&seasonId={}'
        for team, code in teams.items():
            rosters['{}_{}'.format(team, code)] = self.get(url.format(league_id, code, season))

        return rosters

    def projections(self, subset=None):
        pages = []
        if subset:
            for idx in subset:
                content = self.get(self.projection_urls[idx])
                pages.append(content)
        else:
            for url in self.projection_urls:
                content = self.get(url)
                pages.append(content)

        return pages

    def waiver_wire(self, league_id=302946, team_id=12):

        url = 'http://games.espn.com/ffl/freeagency?leagueId={}&teamId={}'
        # http: // games.espn.com / ffl / freeagency?leagueId = 302946 & teamId = 12  # &context=freeagency&view=overview&version=projections&startIndex=50
        return self.get(url.format(league_id, team_id))

if __name__ == "__main__":
    s = ESPNNFLScraper()
    s.league_rosters()

    #pass
