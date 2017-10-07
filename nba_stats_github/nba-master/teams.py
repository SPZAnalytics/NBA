'''
teams.py
Converts various team name formats to others
Different sites use different names for the same NBA teams
'''

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

_city_to_code = {
    'Atlanta': 'ATL',
    'Boston': 'BOS',
    'Brooklyn': 'BKN',
    'Charlotte': 'CHA',
    'Chicago': 'CHI',
    'Cleveland': 'CLE',
    'Dallas': 'DAL',
    'Denver': 'DEN',
    'Detroit': 'DET',
    'Golden State': 'GSW',
    'Houston': 'HOU',
    'Indiana': 'IND',
    'LA Clippers': 'LAC',
    'LA Lakers': 'LAL',
    'Memphis': 'MEM',
    'Miami': 'MIA',
    'Milwaukee': 'MIL',
    'Minnesota': 'MIN',
    'New Jersey': 'NJN',
    'New Orleans': 'NOP',
    'New York': 'NYK',
    'Oklahoma City': 'OKC',
    'Orlando': 'ORL',
    'Philadelphia': 'PHI',
    'Phoenix': 'PHX',
    'Portland': 'POR',
    'Sacramento': 'SAC',
    'San Antonio': 'SAS',
    'Seattle': 'SEA',
    'Toronto': 'TOR',
    'Utah': 'UTA',
    'Washington': 'WAS'
}

_long_to_code = {
    'Atlanta Hawks': 'ATL',
    'Boston Celtics': 'BOS',
    'Brooklyn Nets': 'BKN',
    'Charlotte Hornets': 'CHA',
    'Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL',
    'Denver Nuggets': 'DEN',
    'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU',
    'Indiana Pacers': 'IND',
    'Los Angeles Clippers': 'LAC',
    'Los Angeles Lakers': 'LAL',
    'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA',
    'Milwaukee Bucks': 'MIL',
    'Minnesota Timberwolves': 'MIN',
    'New Jersey Nets': 'NJN',
    'New Orleans Hornets': 'NOH',
    'New Orleans Pelicans': 'NOP',
    'New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL',
    'Philadelphia 76ers': 'PHI',
    'Phoenix Suns': 'PHX',
    'Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC',
    'San Antonio Spurs': 'SAS',
    'Seattle Sonics': 'SEA',
    'Seattle Supersonics': 'SEA',
    'Toronto Raptors': 'TOR',
    'Utah Jazz': 'UTA',
    'Washington Wizards': 'WAS'
}

_ids_to_code = {
    "1610612737": "ATL",
    "1610612738": "BOS",
    "1610612751": "BKN",
    "1610612766": "CHA",
    "1610612741": "CHI",
    "1610612739": "CLE",
    "1610612742": "DAL",
    "1610612743": "DEN",
    "1610612765": "DET",
    "1610612744": "GSW",
    "1610612745": "HOU",
    "1610612754": "IND",
    "1610612746": "LAC",
    "1610612747": "LAL",
    "1610612763": "MEM",
    "1610612748": "MIA",
    "1610612749": "MIL",
    "1610612750": "MIN",
    "1610612740": "NOP",
    "1610612752": "NYK",
    "1610612760": "OKC",
    "1610612753": "ORL",
    "1610612755": "PHI",
    "1610612756": "PHX",
    "1610612757": "POR",
    "1610612758": "SAC",
    "1610612759": "SAS",
    "1610612761": "TOR",
    "1610612762": "UTA",
    "1610612764": "WAS"
}

_code_to_ids = {v:k for k,v in list(_ids_to_code.items())}
_code_to_ids['NOH'] = "1610612740"
_code_to_ids['NOK'] = "1610612740"
_code_to_ids['SEA'] = "1610612760"
_code_to_ids['NJN'] = "1610612751"
_code_to_long = {v:k for k,v in list(_long_to_code.items())}

def city_to_code(name):
    return _city_to_code.get(name)

def long_to_code(name):
    return _long_to_code.get(name)

def id_to_code(id):
    return _ids_to_code.get(id)

def code_to_id(code):
    return _code_to_ids.get(code)

def code_to_long(code):
    return _code_to_long.get(code)

if __name__ == '__main__':
    pass