'''
dkxref.py
cross-reference draftkings players with nfl.player table ids

Usage:
    import logging
    import os
    import pandas as pd
    import dkxref
    logging.basicConfig(level=logging.ERROR)
    from nfl.db.nflpg import NFLPostgres
    nflp = NFLPostgres(database='nfl', user=os.environ.get('NFLPGUSER'), password=os.environ.get('NFLPGPASSWORD'))
    dkp = get_player_id(nflp, pd.read_csv(os.path.join(os.path.expanduser('~'), 'Downloads/DKSalaries.csv')))
'''

import logging

def _dkkey(x):
    return x['Name'].strip() + '_' + x['Position'].strip()

def _first_last(n, fmt='fcl'):
    if fmt == 'fcl':
        parts = n.split(', ')
        return parts[1].strip() + ' ' + parts[0].strip()
    else:
        return n

def _player_id(x, dkp):
    '''
    DKP is a dict - key = site_player_id, value is dict with key player_id
    Used in pd.apply to generate string of the nfl.player player_id
    Can't use integers due to NA values
    '''
    key = x['dk_key'])
    try:
        return str(dkp[key]['player_id'])
    except:
        return None

def get_dk_xref(nflp):
    ## make dk dict
    ## can now use in processing ffa projection files
    q = "SELECT * FROM player_xref WHERE site='dk';"
    return {row['site_player_id']: row for row in nflp.select_dict(q)}

def get_player_id(nflp, df):
    ## takes df, adds player_id from nfl.player table
    df['dk_key'] = df.apply(_dkkey, axis=1)
    dkp = get_dk_xref(nflp)
    df['player_id'] = df.apply(_player_id, axis=1, args=(dkp,))
    return df

def update_dk_xref(nflp, fn):
    '''
    Maps DK dk_key to nfl.player player_id
    '''
    
    ## step one: create dict from existing db - name_pos is key, entire dict is value
    cp = {}
    q = 'SELECT player_id, name, "position", team FROM player'
    for p in nflp.select_dict(q):
        fl = _first_last(p.get('name', ''))
        pid = fl + '_' + p.get('position', '')
        cp[pid] = p

    ## step two: read in DK names
    df = pd.read_csv(fn)
    df['dk_key'] = df.apply(_dkkey, axis=1)
    dkp = df.T.to_dict().values()

    ## step three: compare
    # fields: player_id, site, site_player_id, site_player_name, site_player_team, site_player_position
    for d in dkp:
        k = d.get('dk_key')
        if cp.has_key(k):
            cp[k]['site'] = 'dk'
            cp[k]['site_player_id'] = k
            cp[k]['site_player_name'] = d.get('Name')
            cp[k]['site_player_team'] = d.get('team')
            cp[k]['site_player_position'] = d.get('Position')

    ## step four: insert into db
    ## some inserts will fail, so want to do individual rather than batch
    for v in cp.values():
        nflp.insert_dicts([v], 'player_xref')
              
if __name__ == '__main__':
    pass
