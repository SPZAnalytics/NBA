# espn.py
# functions to transform espn data
# for insertion into database, etc.

from __future__ import print_function
import logging

from fuzzywuzzy import process


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

def match_players(db):
    fixed = []
    nbap = {p['display_first_last']: p['nbacom_player_id'] for p in db.select_dict("""SELECT * FROM playersnodup""")}
    for p in db.select_dict("""SELECT * FROM players_espn"""):
        if nbap.get(p.get('player_name', None), None):
            p['nbacom_player_id'] = nbap[p['player_name']]
        else:
            name, perc = process.extractOne(p.get('player_name', None), list(nbap))
            if perc >= 90:
                p['nbacom_player_id'] = nbap[name]

        if 'nbacom_player_id' in p:
            fixed.append(p)
        else:
            print('could not match {}'.format(p))
    return fixed

def player_xref_table(items):
    ps = []
    for i in items:
        p = {'source': 'espn'}
        p['nbacom_player_id'] = i.get('nbacom_player_id')
        p['source_player_name'] = i.get('player_name')
        p['source_player_id'] = i.get('player_id')
        url = i.get('player_url')
        if url and '/' in url:
            p['source_player_code'] = url.split('/')[-1]
        ps.append(p)
    return ps

if __name__ == '__main__':
    pass