'''
rotowirexref.py
cross-reference rotowire ids with nfl.player table ids

Usage:
    import logging
    import os
    import pandas as pd
    import rwxref
    logging.basicConfig(level=logging.ERROR)
    from nfl.db.nflpg import NFLPostgres
    nflp = NFLPostgres(database='nfl', user=os.environ.get('NFLPGUSER'), password=os.environ.get('NFLPGPASSWORD')

'''

import logging
import re

from bs4 import BeautifulSoup


def _rwkey(x):
    '''
    Used in pd.apply to generate name_position key
    '''
    return x['First Name'].strip() + ' ' + x['First Name'].strip() + '_' + x['position'].strip()

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

def _player_id(x, rwp):
    '''
    Used in pd.apply to generate string of the nfl.player player_id
    Can't use integers due to NA values
    '''
    key = str(x['playerId'])
    try:
        return str(rwp[key]['player_id'])
    except:
        return None

def get_rw_xref(nflp):
    ## make rw dict
    ## can now use in processing rw projection files
    q = "SELECT * FROM player_xref WHERE site='rwnalytics';"
    return {row['site_player_id']: row for row in nflp.select_dict(q)}

def get_player_id(nflp, df):
    ## takes df, adds player_id from nfl.player table
    df['rw_key'] = df.apply(_rwkey, axis=1)
    rwp = get_rw_xref(nflp)
    df['player_id'] = df.apply(_player_id, axis=1, args=(rwp,))
    return df
    
def update_rw_xref(nflp, fn):
    '''
    Maps fantasyfootballanalytics playerId to nfl.player player_id
    '''
    
    ## step one: create dict from existing db
    ## name_pos is key, entire dict is value
    cp = {}
    q = 'SELECT player_id, name, "position", team FROM player'
    for p in nflp.select_dict(q):
        fl = _first_last(p.get('name', ''))
        pid = fl + '_' + p.get('team', '')
        cp[pid] = p

    ## step two: read in rw names
    rwps = []

    with open(fn, 'r') as infile:
        content = infile.read()

    soup = BeautifulSoup(content, 'lxml')

    for p in soup.findAll('p', {'class': 'rank-playername'}):
        rwp = {}
        a = p.find('a')
        rwp['site'] = 'rotowire'
        rwp['site_player_name'] = a.text
        rwp['site_player_id'] = a['href'].split('=')[-1]
        b = p.findAll('b')[-1]
        rwp['team'] = b.text.replace('(', '').replace(')', '')
        rwp['rwp_key'] = a.text + '_' + rwp['team']
        rwps.append(rwp)

    ## step three: compare
    # fields: player_id, site, site_player_id, site_player_name, site_player_team, site_player_position
    for p in rwps:
        k = p.get('rwp_key')

        if cp.has_key(k):
            cp[k]['site'] = 'rotowire'
            cp[k]['site_player_id'] = p.get('site_player_id')
            cp[k]['site_player_name'] = p.get('site_player_name')
            cp[k]['site_player_team'] = p.get('team')
            cp[k].pop('name', '')
            cp[k].pop('position', '')
            cp[k].pop('team', '')


    ## step four: insert into db
    ## some inserts will fail, so want to do individual rather than batch
    for v in cp.values():
        if v.has_key('site_player_id'):
            nflp.insert_dicts([v], 'player_xref')

if __name__ == '__main__':
    pass
    #from nfl.db.nflpg import NFLPostgres
    #nflp = NFLPostgres()
    #update_rw_xref(nflp, fn')
