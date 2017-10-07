from collections import defaultdict
import datetime as dt
import logging
import time

from future.utils import listitems

from nba.parsers.fantasylabs import FantasyLabsNBAParser
from nba.scrapers.fantasylabs import FantasyLabsNBAScraper
from nba.dates import convert_format, datetostr, date_list
from nba.names import match_player


class FantasyLabsNBAAgent(object):
    '''
    Performs script-like tasks using fantasylabs scraper, parser, and db module

    Examples:
        a = FantasyLabsNBAAgent(db=db, cache_name='flabs-agent')
        players = a.today_models()
    '''

    def __init__(self, db, cookies=None, cache_name=None):
        '''
        Args:
            db:
            cookies:
            cache_name:
        '''
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        self.scraper = FantasyLabsNBAScraper(cookies=cookies, cache_name=cache_name)
        self.parser = FantasyLabsNBAParser()
        if db:
            self.db = db
            self.insert_db = True
        else:
            self.insert_db=False


    def one_model(self, model_day, model_name='default'):
        '''
        Gets list of player models for day

        Args:
            model_day (str): in %Y-%m-%d format
            model_name (str): default, cash, etc.
            insert_db (bool): true if want to insert models into database

        Returns:
            players (list): parsed model

        Examples:
            a = FantasyLabsNBAAgent()
            model = a.one_model(model_day='03_01_2016')
        '''
        model = self.scraper.model(model_day=model_day, model_name=model_name)
        players = self.parser.model(content=model, site='dk', gamedate=model_day)

        # need to run through pipeline
        if self.insert_db:
            self.db.insert_salaries(players)
        return players


    def many_models(self, model_name='default', range_start=None, range_end=None, all_missing=False):
        '''
        TODO: is not implemented
        Gets list of player models for day

        Args:
            range_start (str): in %Y-%m-%d format
            range_end (str): in %Y-%m-%d format
            model_name (str): default, cash, etc.

        Returns:
            players (list): parsed model

        Examples:
            a = FantasyLabsNBAAgent()
            models = a.many_models(range_start='2016-03-01', range_end='2016-03-07')
            models = a.many_models(all_missing=True)
        '''
        pass

        '''
        players = []
        if all_missing:
            # THIS NEEDS TO BE ADAPTED
            salaries = []
            for day in self.db.select_list('SELECT game_date FROM missing_salaries'):
                daystr = dt.datetime.strftime(day, '%m_%d_%Y')
                sals = self.parser.dk_salaries(self.scraper.model(daystr), daystr)
                salaries.append(sals)
                if self.insert_db:
                    self.db.insert_salaries(sals)
            return [item for sublist in salaries for item in sublist]
        else:
            for d in date_list(range_end, range_start):
                p = self.one_model(model_day=dt.datetime.strftime(d, '%m_%d_%Y'), model_name=model_name)
                if self.insert_db:
                    self.db.insert_models(p)
                players.append(p)
        return [item for sublist in players for item in sublist]
        '''


    def ownership(self, day=None, all_missing=False):
        '''
        Args:
            day(str): in mm_dd_YYYY format
            all_missing(bool): single day or all missing days in season?
        Returns:
            players(list): of player ownership dict
        '''
        if day:
            day = convert_format(day, 'fl')
            own = self.scraper.ownership(day)
            if self.insert_db:
                self.db.insert_ownership(own, convert_format(day, 'std'))
            return own
        elif all_missing:
            owns = {}
            for day in self.db.select_list('SELECT game_date FROM missing_ownership'):
                daystr = datetostr(day, 'fl')
                own = self.scraper.ownership(daystr)
                self.db.insert_ownership(own, convert_format(daystr, 'std'))
                owns[daystr] = own
            return owns
        else:
            raise ValueError('must provide day or set all_missing to True')


    def salaries(self, day=None, all_missing=False):
        '''
        Args:
            day(str): in mm_dd_YYYY format
        Returns:
            players(list): of player dict
        '''
        if day:
            sals = self.parser.dk_salaries(self.scraper.model(day), day)
            if self.insert_db:
                self.db.insert_salaries(sals, game_date=convert_format(day, 'std'))
            return sals
        elif all_missing:
            salaries = {}
            for day in self.db.select_list('SELECT game_date FROM missing_salaries'):
                daystr = datetostr(day, 'fl')
                sals = self.parser.dk_salaries(self.scraper.model(daystr), daystr)
                salaries[datetostr(day, 'nba')] = sals
                logging.debug('got salaries for {}'.format(daystr))
                time.sleep(1)
            if self.insert_db and salaries:
                self.db.insert_salaries_dict(salaries)
            return salaries
        else:
            raise ValueError('must provide day or set all_missing to True')


    def today_model(self, model_name='default'):
        '''
        Gets list of player models for today's games

        Args:
            model_name (str): default, cash, etc.

        Returns:
            players (list): parsed model

        Examples:
            a = FantasyLabsNBAAgent()
            models = a.today_model()
        '''
        today = dt.datetime.strftime(dt.datetime.today(), '%m_%d_%Y')
        model = self.scraper.model(model_day=today, model_name=model_name)
        return self.parser.model(content=model, gamedate=today)


    def update_player_xref(self):
        '''
        Adds missing players to player_xref table and updates dfs_salaries afterwards
        '''
        nbapq = """SELECT nbacom_player_id as id, display_first_last as n FROM players"""
        nbadict = {}
        nbacount = defaultdict(int)
        for p in self.db.select_dict(nbapq):
            nbadict[p['id']] = p['n']
            nbacount[p['n']] += 1

        # update table
        updateq = """UPDATE dfs_salaries SET nbacom_player_id = sq.nbacom_player_id
                     FROM (SELECT nbacom_player_id, source, source_player_id from player_xref) AS sq
                     WHERE dfs_salaries.nbacom_player_id IS NULL
                     AND dfs_salaries.source_player_id = sq.source_player_id
                     AND dfs_salaries.source = sq.source;"""
        self.db.update(updateq)

        # loop through missing players
        # filter out players with duplicate names - need to manually resolve those
        # then look for direct match where name is not duplicated
        # then try to match using names
        missingq = """SELECT * FROM missing_salaries_ids"""
        insq = """INSERT INTO player_xref (nbacom_player_id, source, source_player_id, source_player_name) VALUES ({}, 'fantasylabs', {}, '{}');"""

        for p in self.db.select_dict(missingq):
            if nbacount[p['n']] > 1:
                logging.error('need to manually resolve {}'.format(p))
                continue
            match = [k for k,v in listitems(nbadict) if v == p['n']]
            if match:
                self.db.update(insq.format(match[0], p['id'], p['n']))
                logging.info('added to xref: {}'.format(p))
                continue
            match = [k for k,v in listitems(nbadict) if v == match_player(p['n'], list(nbadict.values()), threshold=.8)]
            if match:
                self.db.update(insq.format(match[0], p['id'], p['n']))
                logging.info('added to xref: {}'.format(p))
            else:
                logging.error('need to manually resolve {}'.format(p))

        # now update dfs_salaries nbacom_player_id from player_xref
        self.db.update(updateq)


if __name__ == '__main__':
    pass