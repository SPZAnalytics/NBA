'''
teams.py
Converts various team name formats to others
Different sites use different names for the same NBA teams
'''

import logging

t = {
'city_to_code': {
    'Arizona': 'ARI',
    'Atlanta': 'ATL',
    'Baltimore': 'BAL',
    'Buffalo': 'BUF',
    'Carolina': 'CAR',
    'Chicago': 'CHI',
    'Cincinnati': 'CIN',
    'Cleveland': 'CLE',
    'Dallas': 'DAL',
    'Denver': 'DEN',
    'Detroit': 'DET',
    'Green Bay': 'GB',
    'Houston': 'HOU',
    'Indianapolis': 'IND',
    'Jacksonville': 'JAC',
    'Kansas City': 'KC',
    'Los Angeles': 'LARM',
    'Miami': 'MIA',
    'Minnesota': 'MIN',
    'New England': 'NE',
    'New Orleans': 'NO',
    'New York Giants': 'NYG',
    'New York Jets': 'NYJ',
    'NY Giants': 'NYG',
    'NY Jets': 'NYJ',
    'Oakland': 'OAK',
    'Philadelphia': 'PHI',
    'Pittsburgh': 'PIT',
    'San Diego': 'SD',
    'San Francisco': 'SF',
    'Seattle': 'SEA',
    'Tampa Bay': 'TB',
    'Tampa': 'TB',
    'Tennessee': 'TEN',
    'Washington': 'WAS'
},

'long_to_code': {
    'Arizona Cardinals': 'ARI',
    'Atlanta Falcons': 'ATL',
    'Baltimore Ravens': 'BAL',
    'Buffalo Bills': 'BUF',
    'Carolina Panthers': 'CAR',
    'Chicago Bears': 'CHI',
    'Cincinnati Bengals': 'CIN',
    'Cleveland Browns': 'CLE',
    'Dallas Cowboys': 'DAL',
    'Denver Broncos': 'DEN',
    'Detroit Lions': 'DET',
    'Green Bay Packers': 'GB',
    'Houston Texans': 'HOU',
    'Indianapolis Colts': 'IND',
    'Jacksonville Jaguars': 'JAC',
    'Kansas City Chiefs': 'KC',
    'Los Angeles Rams': 'LARM',
    'Miami Dolphins': 'MIA',
    'Minnesota Vikings': 'MIN',
    'New England Patriots': 'NE',
    'New Orleans Saints': 'NO',
    'New York Giants': 'NYG',
    'New York Jets': 'NYJ',
    'Oakland Raiders': 'OAK',
    'Philadelphia Eagles': 'PHI',
    'Pittsburgh Steelers': 'PIT',
    'San Diego Chargers': 'SD',
    'San Francisco 49ers': 'SF',
    'Seattle Seahawks': 'SEA',
    'Tampa Bay Buccaneers': 'TB',
    'Tennessee Titans': 'TEN',
    'Washington Redskins': 'WAS'
},

'nickname_to_code': {
    'Cardinals': 'ARI',
    'Falcons': 'ATL',
    'Ravens': 'BAL',
    'Bills': 'BUF',
    'Panthers': 'CAR',
    'Bears': 'CHI',
    'Bengals': 'CIN',
    'Browns': 'CLE',
    'Cowboys': 'DAL',
    'Broncos': 'DEN',
    'Lions': 'DET',
    'Packers': 'GB',
    'Texans': 'HOU',
    'Colts': 'IND',
    'Jaguars': 'JAC',
    'Chiefs': 'KC',
    'Rams': 'LARM',
    'Dolphins': 'MIA',
    'Vikings': 'MIN',
    'Patriots': 'NE',
    'Saints': 'NO',
    'Giants': 'NYG',
    'Jets': 'NYJ',
    'Raiders': 'OAK',
    'Eagles': 'PHI',
    'Steelers': 'PIT',
    'Chargers': 'SD',
    '49ers': 'SF',
    'Seahawks': 'SEA',
    'Buccaneers': 'TB',
    'Titans': 'TEN',
    'Redskins': 'WAS'
}
}

def city_to_code(name):
    return t['city_to_code'].get(name, None)

def long_to_code(name):
    return t['long_to_code'].get(name, None)

def nickname_to_code(name):
    return t['nickname_to_code'].get(name, None)

if __name__ == '__main__':
    pass
