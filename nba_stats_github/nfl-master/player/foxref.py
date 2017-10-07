'''
foxref.py
cross-reference football outsiders players with nfl.player table ids

Usage:
    import logging
    import foxref

    logging.basicConfig(level=logging.ERROR)
    from nfl.db.nflpg import NFLPostgres
    nflp = NFLPostgres()
    dkp = get_player_id(nflp, pd.read_csv(os.path.join(os.path.expanduser('~'), 'Downloads/DKSalaries.csv')))
'''

import logging
import pprint

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
        return None

def update_fo_xref(nflp, fo_players):
    '''
    Maps fo to nfl.player player_id
    '''
    
    ## step one: create dict from existing db - name_team_pos is key, entire dict is value
    cp = {}
    q = '''
        SELECT
          player_id, first_name, last_name, "position", team
        FROM
          player
        WHERE
          first_name is not null and last_name is not null and "position" != 'UNK' and team != 'UNK'
    '''

    for p in nflp.select_dict(q):
        if p:
            fl = p.get('first_name')[0] + '.' + p.get('last_name')
            pid = '_'.join([fl, p.get('team'), p.get('position')])
            cp[pid] = p

    ## step three: compare
    ## keys: 'player', 'team', 'position'
    for p in fo_players:
        name = p.get('player', ' - ').split('-')[1]
        k = '_'.join([name, p.get('team'), p.get('position')])
        if cp.has_key(k):
            cp[k]['site'] = 'fo_snapcounts'
            cp[k]['site_player_id'] = k
            cp[k]['site_player_name'] = p['player']
            cp[k]['site_player_team'] = p['team']
            cp[k]['site_player_position'] = p['position']
            cp[k]['total_snaps'] = p['total_snaps']
            cp[k]['def_snap_pct'] = float(p['def_snap_pct'].replace('%','')) / 100
            cp[k]['def_snaps'] = p['def_snaps']
            cp[k]['off_snap_pct'] = float(p['off_snap_pct'].replace('%','')) / 100
            cp[k]['off_snaps'] = p['off_snaps']
            cp[k]['st_snap_pct'] = float(p['st_snap_pct'].replace('%','')) / 100
            cp[k]['st_snaps'] = p['st_snaps']
            cp[k]['started'] = p['started'] == 'YES'
            cp[k]['season'] = p['season']
            cp[k]['week'] = p['week']

    ## step four: insert into db
    ## some inserts will fail, so want to do individual rather than batch
    for v in cp.values():
        if v.has_key('total_snaps'):
            nflp.insert_dicts([v], 'snapcounts')
              
if __name__ == '__main__':
    pass

    '''
    logging.basicConfig(level=logging.DEBUG)
    import pickle
    fo_players = []
    with open('/home/sansbacon/snapcounts.pkl', 'rb') as infile:
        fo_players = [{k: str(v).strip() for k,v in p.items()} for p in pickle.load(infile)]

    from nfl.db.nflpg import NFLPostgres
    nflp = NFLPostgres()

    update_fo_xref(nflp, fo_players)
    '''
