import json
import logging

from nba.db.pgsql import NBAPostgres
from nba.pipelines.fantasylabs import salaries_table


class FantasyLabsNBAPg(NBAPostgres):
    '''
    FantasyLabs-specific routines for inserting data into tables
    '''

    def __init__(self, username, password, database = 'nbadb',
                 host = 'localhost', port = 5432):
        '''
        Subclass of NBAPostgres for fantasylabs-specific data
        Args:
            username: str 'nba'
            password: str 'abc123'
            database: str 'nba'
            host: default localhost
            port: defalut 5432
        '''
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        NBAPostgres.__init__(self, user=username, password=password,
                             database=database)


    def insert_models(self, models):
        '''
        TODO: code this out
        '''
        if models:
            self.insert_dicts(models, 'dfs.fantasylabs_models')


    def insert_salaries(self, sals, game_date):
        '''
        Insert list of player salaries into dfs.salaries table

        Args:
            players (list): list of player dictionaries with salaries
        '''
        q = "SELECT DISTINCT source_player_id, nbacom_player_id FROM dfs_salaries WHERE source = 'fantasylabs'"
        allp = {sal.get('source_player_id'): sal.get('nbacom_player_id') for
            sal in self.select_dict(q)}
        self.insert_dicts(salaries_table(sals, game_date), 'dfs_salaries')


    def insert_salaries_dict(self, sals):
        '''
        Insert list of player salaries into dfs.salaries table

        Args:
            players (list): list of player dictionaries with salaries
        '''
        q = "SELECT DISTINCT source_player_id, nbacom_player_id FROM dfs_salaries WHERE source = 'fantasylabs'"
        allp = {sal.get('source_player_id'): sal.get('nbacom_player_id') for
            sal in self.select_dict(q)}

        for k,v in sals.items():
            vals = salaries_table(sals=v, game_date=k)
            self.insert_dicts(vals, 'dfs_salaries')


    def insert_ownership(self, own, game_date):
        '''
        Insert player ownership JSON into table

        Args:
            own: json string
        '''
        cursor = self.conn.cursor()
        try:
            cursor.execute("""INSERT INTO ownership (game_date, data) VALUES (%s, %s);""", (game_date, json.dumps(own)))
            self.conn.commit()
        except Exception as e:
            logging.exception('update failed: {0}'.format(e))
            self.conn.rollback()
        finally:
            cursor.close()




if __name__ == '__main__':
    pass