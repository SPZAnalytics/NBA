'''
ffaxref.py
cross-reference ffanalytics ids with nfl.player table ids

Usage:
    import logging
    import os
    import pandas as pd
    import ffaxref
    logging.basicConfig(level=logging.ERROR)
    from nfl.db.nflpg import NFLPostgres
    nflp = NFLPostgres(database='nfl', user=os.environ.get('NFLPGUSER'), password=os.environ.get('NFLPGPASSWORD')
    ffap = get_player_id(nflp, pd.read_csv(os.path.join(os.path.expanduser('~'), 'Downloads/FFA-CustomRankings.csv')))
'''

import logging


def _ffakey(x):
    '''
    Used in pd.apply to generate name_position key
    '''
    return x['playername'].strip() + '_' + x['position'].strip()

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

def get_ffa_xref(nflp):
    ## make ffa dict
    ## can now use in processing ffa projection files
    q = "SELECT * FROM player_xref WHERE site='ffanalytics';"
    return {row['site_player_id']: row for row in nflp.select_dict(q)}

def get_player_id(nflp, df):
    ## takes df, adds player_id from nfl.player table
    df['ffa_key'] = df.apply(_ffakey, axis=1)
    ffap = get_ffa_xref(nflp)
    df['player_id'] = df.apply(_player_id, axis=1, args=(ffap,))
    return df
    
def update_ffa_xref(nflp, fn):
    '''
    Maps fantasyfootballanalytics playerId to nfl.player player_id
    '''
    
    ## step one: create dict from existing db
    ## name_pos is key, entire dict is value
    cp = {}
    q = 'SELECT player_id, name, "position", team FROM player'
    for p in nflp.select_dict(q):
        fl = _first_last(p.get('name', ''))
        pid = fl + '_' + p.get('position', '')
        cp[pid] = p

    ## step two: read in FFA names
    df = pd.read_csv(fn)       
    df['ffa_key'] = df.apply(_ffakey, axis=1)
    ffap = df.T.to_dict().values()

    ## step three: compare
    # fields: player_id, site, site_player_id, site_player_name, site_player_team, site_player_position
    for p in ffap:
        k = p.get('ffa_key')
        if cp.has_key(k):
            cp[k]['site'] = 'ffanalytics'
            cp[k]['site_player_id'] = p.get('playerId')
            cp[k]['site_player_name'] = p.get('playername')
            cp[k]['site_player_team'] = p.get('team')
            cp[k]['site_player_position'] = p.get('position')
            cp[k].pop('name', '')
            cp[k].pop('position', '')
            cp[k].pop('team', '')

    ## step four: insert into db
    ## some inserts will fail, so want to do individual rather than batch
    for v in cp.values():
        nflp.insert_dicts([v], 'player_xref')

if __name__ == '__main__':
    pass
