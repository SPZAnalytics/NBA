'''
dfs_salaries.py
fetches dfs salaries from fantasylabs from days where database has no salaries
inserts salaries from missing days into dfs_salaries table
'''

import logging
import os
import sys
import time

import browsercookie
from configparser import ConfigParser

from nba.agents.fantasylabs import FantasyLabsNBAAgent
from nba.dates import datetostr
from nba.db.fantasylabs import FantasyLabsNBAPg

logger = logging.getLogger('nbadb-update')
hdlr = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.propagate = False

config = ConfigParser()
configfn = os.path.join(os.path.expanduser('~'), '.nbadb')
config.read(configfn)

flpg = FantasyLabsNBAPg(username=config['nbadb']['username'],
                        password=config['nbadb']['password'],
                        database=config['nbadb']['database'])
fla = FantasyLabsNBAAgent(db=flpg, cache_name='flabs-nba', cookies=browsercookie.firefox())
fla.update_player_xref()

q = """select distinct game_date from games where season = 2015 AND season_type = 'regular' order by game_date DESC"""
for d in flpg.select_list(q):
    try:
        fla.salaries(day=datetostr(d, site='fl'))
        logger.info('completed {}'.format(d))
    except Exception as e:
        logger.exception('{} failed: {}'.format(d, e))
    finally:
        time.sleep(1.5)