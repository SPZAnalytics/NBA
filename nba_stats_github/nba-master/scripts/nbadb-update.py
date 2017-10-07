#!/usr/bin/env python
# updates nbadb tables
# can run on daily or periodic basis

import logging
import os
import sys

from configparser import ConfigParser

from nba.agents.nbacom import NBAComAgent
from nba.db.nbacom import NBAComPg
from nba.db.fantasylabs import FantasyLabsNBAPg
from nba.dates import today


def main():
    #logger = logging.getLogger('nbadb-update')
    #hdlr = logging.StreamHandler(sys.stdout)
    #formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    #hdlr.setFormatter(formatter)
    #logger.addHandler(hdlr)
    #logger.setLevel(logging.INFO)
    #logger.propagate = False
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    config = ConfigParser()
    configfn = os.path.join(os.path.expanduser('~'), '.nbadb')
    config.read(configfn)
    nbapg = NBAComPg(username=config['nbadb']['username'],
                    password=config['nbadb']['password'],
                    database=config['nbadb']['database'])
    flpg = FantasyLabsNBAPg(username=config['nbadb']['username'],
                    password=config['nbadb']['password'],
                    database=config['nbadb']['database'])

    cn = 'nba-agent-{}'.format(today())
    a = NBAComAgent(cache_name=cn, cookies=None, db=nbapg)
    a.scraper.delay = 2
    season = '2016-17'

    # ensures players table is up-to-date before inserting gamelogs, etc.
    a.new_players(season)
    logging.info('finished update nba.com players')

    # gets all missing (days) salaries from current seasons
    from nba.agents.fantasylabs import FantasyLabsNBAAgent
    fla = FantasyLabsNBAAgent(db=flpg, cache_name='flabs-nba')
    fla.salaries(all_missing=True)
    logging.info('finished dfs salaries')

    # ensures that player_xref table includes all players from salaries
    fla.update_player_xref()
    logging.info('finished update player_xref')

    # gets ownership data from fantasylabs
    fla.ownership(all_missing=True)
    logging.info('finished dfs ownership')

    # player_gamelogs
    a.player_gamelogs(season)
    logging.info('finished nba.com player gamelogs')

    # playerstats_daily
    ps = a.playerstats(season, all_missing=True)
    logging.info('finished playerstats daily')

    # update team_gamelogs
    a.team_gamelogs(season)
    logging.info('finished team gamelogs')

    # teamstats_daily
    a.teamstats(season, all_missing=True)
    logging.info('finished teamstats daily')

    # team_opponent_dashboards
    a.team_opponent_dashboards(season, all_missing=True)
    logging.info('finished team_opponent_dashboards')

    # refresh all materialized views
    refreshq = """SELECT RefreshAllMaterializedViews('*');"""
    nbapg.execute(refreshq)


if __name__ == '__main__':
    main()