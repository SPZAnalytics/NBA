'''
fprosxref.py
cross-reference fantasypros ids with nfl.player table ids

Usage:
    import logging
    import os
    import pandas as pd
    import fprosxref
    logging.basicConfig(level=logging.ERROR)
    from nfl.db.nflpg import NFLPostgres
    nflp = NFLPostgres(database='nfl', user=os.environ.get('NFLPGUSER'), password=os.environ.get('NFLPGPASSWORD')
    fpros = get_player_id(nflp, pd.read_csv(os.path.join(os.path.expanduser('~'), 'Downloads/FFA-CustomRankings.csv')))
'''

import json
import pprint

import pandas as pd

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

def update_fpros_xref(nflp, fn):
    '''
    Maps fantasypros playerid to nfl.player player_id
    '''
    
    ## step one: create dict from existing db
    ## name_pos is key, entire dict is value
    cp = {}
    q = 'SELECT player_id, name, "position", team FROM player'
    for p in nflp.select_dict(q):
        fl = _first_last(p.get('name', ''))
        pid = fl + '_' + p.get('position', '')
        cp[pid] = p

    ## step two: read in fpros names
    df = pd.read_json(fn)
    df['fp_key'] = df.apply(_fpkey, axis=1)
    ffap = df.T.to_dict().values()

    ## step three: compare
    # fields: player_id, site, site_player_id, site_player_name, site_player_team, site_player_position
    for p in ffap:
        k = p.get('fp_key')
        if cp.has_key(k):
            cp[k]['site'] = p.get('site')
            cp[k]['site_player_id'] = p.get('site_player_id')
            cp[k]['site_player_name'] = p.get('site_player_name')
            cp[k]['site_player_team'] = p.get('team')
            cp[k]['site_player_position'] = p.get('pos')
            cp[k].pop('team', '')
            cp[k].pop('name', '')
            cp[k].pop('position', '')

    pprint.pprint(cp)

    ## step four: insert into db
    ## some inserts will fail, so want to do individual rather than batch
    #for v in cp.values():
    #    nflp.insert_dicts([v], 'player_xref')

if __name__ == '__main__':
    pass
    '''
    import logging
    import os
    import pandas as pd

    logging.basicConfig(level=logging.ERROR)
    from nfl.db.nflpg import NFLPostgres
    nflp = NFLPostgres()
    update_fpros_xref(nflp, '/home/sansbacon/fpros-players.json')
    '''
