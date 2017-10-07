from __future__ import absolute_import

from configparser import ConfigParser
from datetime import datetime as dt
import os
import random
import unittest

from nba.agents.fantasylabs import FantasyLabsNBAAgent
from nba.db.fantasylabs import FantasyLabsNBAPg
from nba.dates import *

class FantasyLabsNBAAgent_test(unittest.TestCase):

    def setUp(self):
        self.today = dt.strftime(dt.today(), '%-m_%-d_%Y')
        self.config = ConfigParser()
        configfn = os.path.join(os.path.expanduser('~'), '.nbadb')
        self.config.read(configfn)
        self.db = FantasyLabsNBAPg(username=self.config['nbadb']['username'],
                                password=self.config['nbadb']['password'],
                                database=self.config['nbadb']['database'])
        self.a = FantasyLabsNBAAgent(cache_name='testflabs-nba', db=self.db)

    def test_init(self):
        # this should fail
        # adb = FantasyLabsNBAAgent(db=True)
        adb = FantasyLabsNBAAgent(cache_name='testnba', db=self.db)
        self.assertIsNotNone(adb.scraper)
        self.assertIsNotNone(adb.parser)
        self.assertIsNotNone(adb.db)

    def test_salaries(self):
        model = self.a.scraper.model(self.today)
        q = """SELECT DISTINCT source_player_id, nbacom_player_id FROM dfs_salaries WHERE source = 'fantasylabs'"""
        allp = {sal.get('source_player_id'): sal.get('nbacom_player_id') for
                sal in self.db.select_dict(q)}

        for p in self.a.parser.model(model):
            print(p.get('Player_Name'), allp.get(int(p.get('PlayerId', 0))))

    '''
    def test_past_day_models(self):
        delta = random.choice(range(1,7))
        d = dt.datetime.today() - dt.timedelta(delta)
        fmt = site_format('fl')
        models, pp_models = self.a.past_day_models(model_day=dt.datetime.strftime(d, fmt))
        logging.debug('there are {0} models'.format(len(models)))
        self.assertIsInstance(models, list)
        self.assertTrue(len(models) > 0)
        model = random.choice(models)
        self.assertIsInstance(model, dict)
        self.assertIn('Salary', model)

        pp_model = random.choice(pp_models)
        self.assertIsInstance(pp_model, dict)
        self.assertIn('salary', pp_model)


    def test_range_models(self):
        fmt = site_format('fl')
        delta = random.choice(range(7,14))
        range_start = dt.datetime.today() - dt.timedelta(delta)
        range_end = range_start + dt.timedelta(2)

        models, pp_models = self.a.range_models(range_start=dt.datetime.strftime(range_start, fmt),
                                                range_end=dt.datetime.strftime(range_end, fmt))

        logging.debug('there are {0} models'.format(len(models)))
        self.assertIsInstance(models, list)
        self.assertTrue(len(models) > 0)
        model = random.choice(models)
        self.assertIsInstance(model, dict)
        self.assertIn('Salary', model)

        pp_model = random.choice(pp_models)
        self.assertIsInstance(pp_model, dict)
        self.assertIn('salary', pp_model)

    def test_today_model(self):
        models, pp_models = self.a.today_model()
        logging.debug('there are {0} models'.format(len(models)))
        self.assertIsInstance(models, list)
        self.assertTrue(len(models) > 0)
        model = random.choice(models)
        self.assertIsInstance(model, dict)
        self.assertIn('Salary', model)

        pp_model = random.choice(pp_models)
        self.assertIsInstance(pp_model, dict)
        self.assertIn('salary', pp_model)
    '''

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()