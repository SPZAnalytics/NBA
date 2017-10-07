'''
flabsxref.py
cross-reference fantasylabs players with nfl.player table ids

Usage:
    import logging
    import os
    import pandas as pd
    import flabsxref
    logging.basicConfig(level=logging.ERROR)
    from nfl.db.nflpg import NFLPostgres
    nflp = NFLPostgres(database='nfl', user=os.environ.get('NFLPGUSER'), password=os.environ.get('NFLPGPASSWORD'))

'''

import logging
import pprint

import pandas as pd


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

def _sitekey(x):
    return x['player'].strip() + '_' + x['pos'].strip()

def get_flabs_xref(nflp):
    ## make flabs dict
    q = "SELECT * FROM player_xref WHERE site='fantasylabs';"
    return {row['site_player_id']: row for row in nflp.select_dict(q)}

def get_player_id(nflp, players):
    # need to rewrite for flabs
    # combine Player_Name, Team, Position
    pass

def update_flabs_xref(nflp, players):
    '''
    Maps fantasylabs PlayerId to nfl.player player_id
    '''

    site = 'fantasylabs'
    
    ## step one: create dict from existing db
    ## name_pos is key, entire dict is value
    cp = {}
    q = 'SELECT player_id, name, "position", team FROM player'
    for p in nflp.select_dict(q):
        fl = _first_last(p.get('name', ''))
        pid = fl + '_' + p.get('position', '')
        cp[pid] = p

    ## step two: read in flabs
    df = pd.DataFrame(players)
    df['site_key'] = df.apply(_sitekey, axis=1)

    ## step three: compare
    # fields: player_id, site, site_player_id, site_player_name, site_player_team, site_player_position
    valid = []
    for p in df.T.to_dict().values():
        k = p.get('site_key')
        if cp.has_key(k):
            cp[k]['site'] = site
            cp[k]['site_player_id'] = p.get('source_player_id')
            cp[k]['site_player_name'] = p.get('player')
            cp[k]['site_player_team'] = p.get('team')
            cp[k]['site_player_position'] = p.get('pos')
            cp[k].pop('team', '')
            cp[k].pop('name', '')
            cp[k].pop('position', '')
            valid.append(cp[k])
        else:
            logging.error(k)

    logging.debug(pprint.pformat(cp))

    ## step four: insert into db
    ## some inserts will fail, so want to do individual rather than batch
    #for v in cp.values():
    #    if v.has_key('site_player_id'):
    for v in valid:
        nflp.insert_dicts([v], 'player_xref')
        
if __name__ == '__main__':
    pass
    #logging.basicConfig(level=logging.ERROR)
    #from nfl.parsers import fantasylabs
    #from nfl.db.nflpg import NFLPostgres
    #nflp = NFLPostgres()
    #p = fantasylabs.FantasyLabsNFLParser()
    #fn = '/home/sansbacon/9_14_2016.json'
    #with open (fn, 'r') as infile:
    #    content = infile.read()
    #players = p.dk_salaries(content=content, season=2016, week=2)
    #update_flabs_xref(nflp, players)
