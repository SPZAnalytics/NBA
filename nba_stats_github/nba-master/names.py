'''
names.py
'''

import re

from fuzzywuzzy import fuzz, process
from nameparser import HumanName


def first_last(name):
    '''
    Returns name in First Last format
    
    '''
    hn = HumanName(name)
    return '{0} {1}'.format(hn.first, hn.last) 


def last_first(name):
    '''
    Returns name in Last, First format
    '''

    hn = HumanName(name)
    return '{1}, {0}'.format(hn.first, hn.last) 


def doug_name(name):
    '''
    Returns string in doug format: last,first, lowercase, no punctuation, 16 character max
    '''
    # all names lowercase
    name = name.lower()

    # get rid of periods and apostrophes
    name = re.sub(r"[.']+", "", name)

    hn = HumanName(name)
    return '{1},{0}'.format(hn.first, hn.last)[0:15] 


def espn_doug (self, espn_names, doug_names):
    '''
    Matches espn names to dougstats names
    Args:
        self:
        espn_names:
        doug_names:

    Returns:

    '''
    matched_names = []
    for name in espn_names:
        parts = name.split(' ')
        if len(parts) > 1:
            dougname = '{0},{1}'.format(parts[1], parts[0])
            dougname = dougname[0:16].lower()
            matched_names.append(match_player(dougname, doug_names))
    return matched_names


def match_player (to_match, match_from, threshold = .8):
    '''
    Matches player with direct or fuzzy match
    Args:
        to_match (str): player name to match
        match_from (list): list of player names to match against

    Returns:
        name (str): matched name from match_from list

    Example:
        name = match_player(player, players)
    '''
    name = None

    # first see if there is a direct match
    if to_match in match_from:
        name = to_match
    # try first last
    if not name:
        for mf in match_from:
            to_match = first_last(to_match)
            possible_match = first_last(mf)
            if to_match == possible_match:
                name = mf
    # if still no match, then try fuzzy matching
    if not name:
        fuzzy, confidence = process.extractOne(to_match, match_from)
        if confidence >= threshold:
            name = fuzzy
    return name


if __name__ == '__main__':
    pass
