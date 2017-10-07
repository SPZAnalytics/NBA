# pipelines.py
# functions to transform nbacom list of dict
# for insertion into database, use in optimizer, etc.


from __future__ import print_function
from future.utils import iteritems
import logging

from nba.dates import convert_format, datetostr, strtodate
from nba.dfs import dk_points, fd_points

logging.getLogger(__name__).addHandler(logging.NullHandler())


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


def players_table(players):
    '''
    Prepares players for insertion into nbadb players table

    Args:
        players: list of dict

    Returns:
        List of dict formatted for insertion into database
    '''
    fixed = []

    # get rid of extraneous columns, use different names for person_id and position
    omit = ['display_fi_last', 'display_last_comma_first', 'dleague_flag', 'games_played_flag', 'nbacom_team_id',
            'playercode', 'rosterstatus', 'season_exp', 'team_abbreviation', 'team_city', 'team_code', 'team_id', 'team_name']
    convert = {'person_id': 'nbacom_player_id', 'position': 'nbacom_position'}

    # loop through players
    # use lowercase key names, fix values for various columns
    # height (in inches) needs to be calculated from 6-10
    # replace 'Undrafted' or non-integer draft positions with None
    # if player is C, can add primary_position and position_group
    for p in players:
        fp = {}
        for k,v in p.items():
            nk = k.lower()
            if nk in omit:
                continue
            elif nk in convert:
                nk = convert[nk]
            elif nk == 'height':
                try:
                    f,i = v.split('-')
                    v = int(f) * 12 + int(i)
                except:
                    v = None
            elif 'draft' in nk:
                try:
                    v = int(v)
                except:
                    v = None
            elif nk == 'nbacom_position':
                if v == 'C':
                    fp['position_group'] = 'Big'
                    fp['primary_position'] = 'C'
            if v == '':
                v = None
            fp[nk] = v
        fixed.append(fp)
    return fixed


def player_boxscores_table(pbs):
    '''
    Cleans merged list of player boxscores

    Arguments:
        pbs: list of playerboxscore dictionaries

    Returns:
        cleaned_players: list of playerboxscore dictionaries
    '''
    omit = ['COMMENT', 'FG3_PCT', 'FG_PCT', 'FT_PCT', 'TEAM_CITY', 'TEAM_NAME']
    cleaned_players = []
    for player in pbs:
        clean_player = {k.lower(): v for k, v in player.iteritems() if k not in omit}
        if clean_player.has_key('to'):
            clean_player['tov'] = clean_player['to']
            clean_player.pop('to', None)
        clean_player.pop('team_abbreviation', None)
        cleaned_players.append(clean_player)
    return cleaned_players


def player_gamelogs_table(gl):
    '''
    Prepares players for insertion into nbadb players table

    Args:
        players: list of dict
    Returns:
        List of dict formatted for insertion into database

    '''
    fixed = []
    omit = ['GAME_DATE', 'VIDEO_AVAILABLE', 'TEAM_NAME', 'MATCHUP', 'WL', 'SEASON_ID']

    for l in gl:
        cl = {k.lower().strip(): v for k, v in l.items() if k.upper() not in omit}
        cl['dk_points'] = dk_points(cl)
        cl['fd_points'] = fd_points(cl)

        # change to nbacom_player_id
        if 'player_id' in cl:
            cl['nbacom_player_id'] = cl['player_id']
            cl.pop('player_id', None)
        if 'team_abbreviation' in cl:
            cl['team_code'] = cl['team_abbreviation']
            cl.pop('team_abbreviation', None)
        fixed.append(cl)
    return fixed


def playerstats_table(ps, as_of):
    '''
    Cleans merged list of player base + advanced stats

    Arguments:
        ps: list of player dictionaries

    Returns:
        cleaned_players: list of player dictionaries
    '''
    omit = ['CFID', 'CFPARAMS', 'COMMENT', 'TEAM_NAME']
    cleaned_players = []
    for player in ps:
        clean_player = {k.lower(): v for k, v in iteritems(player) if k not in omit}
        if 'to' in clean_player:
            clean_player['tov'] = clean_player['to']
            clean_player.pop('to', None)
        if 'team_abbreviation' in clean_player:
            clean_player['team_code'] = clean_player['team_abbreviation']
            clean_player.pop('team_abbreviation', None)
        if 'player_id' in clean_player:
            clean_player['nbacom_player_id'] = clean_player['player_id']
            clean_player.pop('player_id', None)
        clean_player['as_of'] = as_of
        cleaned_players.append(clean_player)
    return cleaned_players


def team_gamelogs_table(tgl):
    '''
    Cleans merged list of team gamelogs base + advanced

    Arguments:
        tgl: list of dictionaries

    Returns:
        cleaned_items(list)
    '''
    omit = ['matchup', 'season_id', 'team_name', 'video_available', 'wl']
    cleaned_items = []
    for gl in tgl:
        cleaned_item = {k.lower(): v for k,v in gl.items() if k.lower() not in omit}
        if cleaned_item.get('team_abbreviation'):
            cleaned_item['team_code'] = cleaned_item['team_abbreviation']
            cleaned_item.pop('team_abbreviation', None)
        if cleaned_item.get('min'):
            cleaned_item['minutes'] = cleaned_item['min']
            cleaned_item.pop('min', None)
        cleaned_items.append(cleaned_item)
    return cleaned_items


def team_opponent_dashboards_table(dash, as_of):
    '''
    Args:
        dash:
        as_of:

    Returns:

    '''
    topp = []
    omit = ['CFID', 'CFPARAMS', 'COMMENT', 'TEAM_NAME']
    for team in dash:
        fixed_team = {k.lower(): v for k, v in team.items() if k not in omit}
        fixed_team.pop('team_name', None)
        fixed_team['as_of'] = convert_format(as_of, 'nba')
        topp.append(fixed_team)
    return topp


def teamstats_table(ts, as_of):
    '''
    Cleans merged list of team base + advanced stats

    Arguments:
        ts: list of dictionaries
        as_of(str): in YYYY-MM-DD format

    Returns:
        cleaned_items(list): list of cleaned team dictionaries
    '''
    omit = ['CFID', 'CFPARAMS', 'COMMENT', 'TEAM_CITY', 'TEAM_NAME']
    if ts:
        cleaned_items = [{k.lower(): v for k,v in iteritems(item) if k not in omit} for item in ts]
        for idx, _ in enumerate(cleaned_items):
            cleaned_items[idx]['as_of'] = as_of
        return cleaned_items
    else:
        logging.error('teamstats_table: ts is None')
        return None


if __name__ == '__main__':
    pass