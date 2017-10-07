# matcher.py
# matches names in different formats
# useful for cross-references
# TODO: this should be generic than can inherit for nfl/nba specific? or just make a class?

from fuzzywuzzy import fuzz, process
import logging
import pprint
import re

logger = logging.getLogger(__name__)

def first_last(name):
    '''
    Turns Last, First into First Last
    :param name (str): in Last, First format
    :return other_name (str): in First Last format
    '''
    if re.match('^\w+[,]+\s+\w+', name):
        (last, first) = [x.strip() for x in name.split(',')]
        name = '%s %s' % (first, last)

    elif re.match (r'^\w+[.]?\w?\s+\w+', name):
        (last, first) = [x.strip() for x in name.split(',')]
        name = '%s %s' % (first, last)

    return name

def is_first_last(name):
    '''

    :param name:
    :return:
    '''
    if re.match('^\w+\s+\w+', name):
        return True
    else:
        return False

def is_last_first(name):
    '''

    :param name:
    :return:
    '''
    if re.match('^\w+[,]+\s?\w+', name):
        return True
    else:
        return False

def last_first(name):
    '''
    Turns Last, First into First Last
    :param name (str): in Last, First format
    :return other_name (str): in First Last format
    '''

    name = name.strip()

    try:
        if re.match(r'^\w+\s+\w+', name):
            (first, last) = name.split()
            name = '%s, %s' % (last, first)
        else:
            pass

    except:
        pass

    return name

def fix_name(name):
    '''

    :param name:
    :return:
    '''
    # all names lowercase
    name = name.lower()

    # get rid of periods and apostrophes
    name = re.sub(r"[.']+", "", name)

    if is_first_last(name):
        logger.debug('is first last')
        full_name = last_first(name)
        name_first_last = name

    elif is_last_first(name):
        logger.debug('is last first')
        full_name = name
        name_first_last = first_last(name)

    else:
        logger.debug('not either one')
        full_name = name
        name_first_last = name

    return full_name, name_first_last

def match_player (to_match, match_from, site_id_key):
    '''
    :param to_match (dictionary): Player dictionary to match
    :param match_from (dictionary): key is player name, value is player
    :return site_id (str):

    Example:
        site_id = NameMatcher.match_player(player, players, 'espn_id')
    '''

    # first see if there is a direct match
    match = match_from.get(to_match['full_name'], None)

    # if no direct match, then try first_last
    if not match:
        match = match_from.get(to_match['first_last'], None)

    # if still no match, then try fuzzy matching
    if not match:
        name, confidence = process.extractOne(to_match['full_name'], match_from.keys())
        logger.debug('name %s | confidence %d' % (name, confidence))

        if confidence > 80:
            match = match_from.get(name, None)
            logger.debug('fuzzy match: %s' % pprint.pformat(match))

            if match.get('position') == to_match.get('position') and match.get('position') is not None:
                to_match[site_id_key] = match.get(site_id_key, None)
            else:
                pass
                #logger.info ('right name, wrong position: to_match %s %s | match_from %s %s'
                #                % (to_match.get('full_name', None), to_match.get('position', None),
                #                   match_from.get('full_name', None), match_from.get('position', None)))
        elif confidence > 50:
            logger.debug('%s | %d' % (name, confidence))
        else:
            logger.debug('%s | %d' % (name, confidence))

    else:
        to_match[site_id_key] = match.get(site_id_key, None)

    return to_match

if __name__ == '__main__':
    pass
