# pipelines.py
# functions to transform fantasylabs data
# for insertion into database, use in optimizer, etc.


from __future__ import print_function
from datetime import datetime as dt
import logging

from nba.seasons import in_what_season
#from pydfs_lineup_optimizer import Player


def isfloat(x):
    try:
        a = float(x)
    except Exception as e:
        return False
    else:
        return True

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except Exception as e:
        return False
    else:
        return a == b

'''
def make_player(p, weights=[.6, .3, .1]):
    name = p.get('Player_Name')
    if name and ' ' in name:
        first, last = name.split(' ')[0:2]
    else:
        first = name
        last = None
    mean = p.get('AvgPts')
    floor = p.get('Floor')
    ceiling = p.get('Ceiling')
    fppg = mean * weights[0] + ceiling * weights[1] + floor * weights[2]

    return Player(
        '',
        first,
        last,
        p.get('Position').split('/'),
        p.get('Team'),
        float(p.get('Salary', 0)),
        fppg
    )
'''

def match_names(a):
    q = """SELECT DISTINCT source_player_id, nbacom_player_id FROM dfs_salaries WHERE source = 'fantasylabs'"""
    allp = {sal.get('source_player_id'): sal.get('nbacom_player_id') for
            sal in a.db.select_dict(q)}

    flplayers = {}

    # lq = """'SELECT game_date FROM missing_salaries"""
    lq = """SELECT distinct game_date FROM games WHERE game_date <= now()::date AND game_date >= '2017-01-01'"""

    for day in a.db.select_list(lq):
        daystr = dt.strftime(day, '%m_%d_%Y')
        for p in a.parser.dk_salaries(a.scraper.model(daystr), daystr):
            if p.get('PlayerId', 0) in allp:
                continue
            else:
                print(p.get('Player_Name'), p.get('PlayerId'))

def optimizer_pipeline(self, models):
    '''
    Takes fantasylabs models, make ready to create Player objects for pydfs_lineup_optimizer

    Args:
        models (list): is parsed json from day's models

    Returns:
        players (list): list of players, fixed for use in pydfs_lineup_optimizer

    Examples:
        a = FantasyLabsNBAAgent()
        models = a.today_models()
        players = a.optimizer_pipeline(models)

    '''
    fl_keys = ['PlayerId', 'Player_Name', 'Position', 'Team', 'Salary', 'Score', 'AvgPts', 'Ceiling', 'Floor',
               'ProjPlusMinus']
    fl_players = [{k: v for k, v in p.items() if k in fl_keys} for p in models]

    # remove null values
    for idx, flp in enumerate(fl_players):
        if flp.get('Ceiling') is None:
            fl_players[idx]['Ceiling'] = 0
        if flp.get('Floor') is None:
            fl_players[idx]['Floor'] = 0
        if flp.get('AvgPts') is None:
            fl_players[idx]['AvgPts'] = 0

    return fl_players

def ownership_table(own, game_date):
    '''
    Transforms salary data into dict to insert into table
    Args:
        sals:
        all_players:
        game_date:

    Returns:
        List of dict to insert into db
    '''
    pass

def salaries_table(sals, game_date):
    '''
    Transforms salary data into dict to insert into table
    Args:
        sals:
        all_players:
        game_date:

    Returns:
        List of dict to insert into db
    '''
    for idx, salary in enumerate(sals):
        fx = {'source': 'fantasylabs', 'dfs_site': 'dk', 'game_date': game_date}
        fx['season'] = in_what_season(game_date, fmt=True)
        fx['source_player_id'] = salary.get('PlayerId')
        fx['source_player_name'] = salary.get('Player_Name')
        fx['salary'] = salary.get('Salary')
        fx['team_code'] = salary.get('Team')
        fx['dfs_position'] = salary.get('Position')
        sals[idx] = fx
    return sals

def preprocess_games(games):
    '''
    TODO: adapt this code to pipeline
    Returns games ready for insert into dfs tables

    Args:
        games (list): list of game dictionaries

    Returns:
        fixed_games (list): list of game dictionaries ready for insert into dfs.salaries

    '''
    pass
    #fixed_games = []
    #wanted_keys = ['EventId', 'EventDateTime', 'EventDate', 'HomeTeamShort', 'VisitorTeamShort',
    #               'ProjHomeScore', 'ProjVisitorScore']

    # get list of games from stats.games
    #sql = '''SELECT game_id, gamecode FROM stats.games'''
    '''
    try:
        nbacom_games = {g['gamecode']: g['game_id'] for g in self.select_dict(sql)}
    except:
        nbacom_games = {}

    if games:
        for game in games:
            fixed_game = {self._convert(k):v for k,v in game.iteritems() if k in wanted_keys}
            away = game['VisitorTeamShort']
            home = game['HomeTeamShort']
            event_date = game.get('EventDate')
            d, t = event_date.split('T')

            if d:
                d = dt.datetime.strftime(dt.datetime.strptime(d, '%Y-%m-%d'), '%Y%m%d')

            gamecode = '{0}/{1}{2}'.format(d, away, home)
            fixed_game['gamecode'] = gamecode
            fixed_game['nbacom_game_id'] = nbacom_games.get(gamecode)
            fixed_games.append(fixed_game)

    return fixed_games

    def _convert(self, s0):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s0)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _nbacom_player_id(self, site_player_id):
        if not self.player_xref:
            self.player_xref = self.nbaplayers.player_xref('fl')

        return self.player_xref.get(site_player_id)
    '''