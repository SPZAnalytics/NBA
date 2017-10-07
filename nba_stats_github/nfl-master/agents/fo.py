import logging
import time

from nfl.parsers.fo import FootballOutsidersNFLParser
from nfl.scrapers.fo import FootballOutsidersNFLScraper
from nfl.player.foxref import update_fo_xref


class FootballOutsidersAgent(object):
    '''
    Usage:

    '''

    def __init__(self, wb=False):
        self._s = FootballOutsidersNFLScraper(cache_name='foagent-cache')
        self._p = FootballOutsidersNFLParser()

    def snap_counts(self, seasons, weeks):
        players = []

        for season in seasons:
            for week in weeks:
                content = self._s.snap_counts(season, week)
                players += self._p.snap_counts(content, season, week)
                time.sleep(1)
        return players

if __name__ == '__main__':
    # TODO: need to figure out what to do about
    # duplicate players and failed matches

    #logging.basicConfig(level=logging.ERROR)
    #a = FootballOutsidersAgent()
    #from nfl.db.nflpg import NFLPostgres
    #nflp = NFLPostgres()

    #
    #for w in range(1,17):
    #    update_fo_xref(nflp, a.snap_counts(seasons=[2015, 2014, 2013, 2012, 2011, 2010], weeks=[w]))

    #q = '''
    #    update snapcounts
    #    set gsis_id = sq.gsis_id
    #    from (select * from cs_teamgames) as sq
    #    where snapcounts.season = sq.season_year AND snapcounts.week = sq.week AND snapcounts.team = sq.team
    #'''

    nflp.update(q)
