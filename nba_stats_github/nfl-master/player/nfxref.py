'''
nfxref.py
cross-reference numberfire ids with nfl.player table ids

Usage:
    import logging
    import os
    import pandas as pd
    import nfxref
    logging.basicConfig(level=logging.ERROR)
    from nfl.db.nflpg import NFLPostgres
    nflp = NFLPostgres(database='nfl', user=os.environ.get('NFLPGUSER'), password=os.environ.get('NFLPGPASSWORD')
    update_nf_xref(nflp, os.path.join(os.path.expanduser('~'), 'numberfire_nfl_players.json'))
'''

import copy
import json
import logging
import pprint


def _fpkey(x):
    '''
    Used in pd.apply to generate name_position key
    '''
    return x['site_player_name'].strip() + '_' + x['pos'].strip()

def _first_last(n, fmt='fcl'):
    '''
    Converts various name formats to first_last
    TODO: this is duplicative of some other module - have done for NBA
    and maybe last year for NFL
    '''
    if fmt == 'fcl':
        parts = n.split(', ')
        return parts[1].strip() + ' ' + parts[0].strip()
    else:
        return n

def _player_id(x, ffap):
    '''
    Used in pd.apply to generate string of the nfl.player player_id
    Can't use integers due to NA values
    '''
    key = str(x['playerId'])
    try:
        return str(ffap[key]['player_id'])
    except:
        return None

def get_fpros_xref(nflp):
    ## make ffa dict
    ## can now use in processing ffa projection files
    q = "SELECT * FROM player_xref WHERE site='ffanalytics';"
    return {row['site_player_id']: row for row in nflp.select_dict(q)}

def get_player_id(nflp, df):
    ## takes df, adds player_id from nfl.player table
    df['fp_key'] = df.apply(_fpkey, axis=1)
    fp = get_fpros_xref(nflp)
    df['player_id'] = df.apply(_player_id, axis=1, args=(fp,))
    return df

def update_nf_xref(nflp, fn):
    '''
    Maps numberfire playerid to nfl.player player_id via espn_id
    '''
    
    ## step one: create dict from existing db
    ## name_pos is key, entire dict is value
    cp = {}
    q = 'SELECT player_id, espn_id FROM player where espn_id > 0'
    for p in nflp.select_dict(q):
        cp[p['espn_id']] = p

    ## step two: read in fpros names
    nf = []
    with open('/home/sansbacon/numberfire_nfl_players.json', 'r') as infile:
        nfplayers = json.load(infile)

    for k, v in nfplayers.items():
        p2 = copy.deepcopy(v)
        p2['numberfire_id'] = k
        nf.append(p2)

    ## step three: compare
    # fields: player_id, site, site_player_id, site_player_name, site_player_team, site_player_position
    matched = []
    for p in nf:
        k = p.get('espn_id')

        try:
            k = int(k)
            if cp.has_key(k):
                cp2 = copy.deepcopy(cp[k])
                cp2['site'] = 'numberfire'
                cp2['site_player_id'] = p.get('numberfire_id')
                cp2['site_player_name'] = p.get('name')
                cp2['site_player_position'] = p.get('position')
                cp2.pop('espn_id', '')
                matched.append(cp2)

        except Exception as e:
            logging.exception(e)

    ## step four: insert into db
    ## some inserts may fail, so want to do individual rather than batch
    for m in matched:
        nflp.insert_dicts([m], 'player_xref')


def update_other_xref(nflp, fn):
    '''
    Maps other ids in numberfire (sports_reference, yahoo) to nfl.player player_id via espn_id
    '''

    ## step one: create dict from existing db
    ## name_pos is key, entire dict is value
    cp = {}
    q = 'SELECT player_id, espn_id FROM player where espn_id > 0'
    for p in nflp.select_dict(q):
        cp[p['espn_id']] = p

    ## step two: read in nf names
    with open('/home/sansbacon/numberfire_nfl_players.json', 'r') as infile:
        nfplayers = json.load(infile)
        nf = nfplayers.values()

    ## step three: compare
    # fields: player_id, site, site_player_id, site_player_name, site_player_team, site_player_position
    matched = []
    for p in nf:
        k = p.get('espn_id')

        try:
            k = int(k)
            if cp.has_key(k):
                cp2 = copy.deepcopy(cp[k])
                cp2['site'] = 'yahoo'
                cp2['site_player_id'] = p.get('yahoo_id')
                cp2['site_player_name'] = p.get('name')
                cp2['site_player_position'] = p.get('position')
                cp2.pop('espn_id', '')
                matched.append(cp2)

        except Exception as e:
            logging.exception(e)

    logging.debug(pprint.pformat(matched[0]))

    ## step four: insert into db
    ## some inserts may fail, so want to do individual rather than batch
    for m in matched:
        nflp.insert_dicts([m], 'player_xref')


if __name__ == '__main__':
    pass