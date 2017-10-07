'''
PlayerProfilerNFLParser
'''

import datetime
import json
import logging
import pprint

from nfl import nflseasons
from nfl import teams

class PlayerProfilerNFLParser:
    '''
    Takes json from scraper, returns list of dict
    '''

    def __init__(self):
        logging.getLogger(__name__).addHandler(logging.NullHandler())


    def player_page(self, content):
        '''
        Parses single player page from playerprofiler
        '''
        try:
            data = json.loads(content)['data']['Player']

        except Exception as e:
            logging.exception('could not load content: {}'.format(e))

        player = {}
        player['site'] = 'playerprofiler'
        player['site_player_id'] = data['Player_ID']

        for idx, cat in enumerate(['College Performance', 'Core', 'Game Logs', 'Medical History', 'Performance Metrics', 'Workout Metrics']):
            continue

        # College performance
            ## Breakout year, breakout age, breakout age rank

        cp = data['College Performance']
        cp_mapping = {'College YPC': 'college_ypc', 'College Target Share Rank': 'college_target_share_rank',
                      'College YPR': 'college_ypr', 'College Dominator Rating Rank': 'college_dominator_rating_rank',
                      'Breakout Year': 'breakout_year', 'College YPC Rank': 'college_ypc_rank',
                      'College YPR Rank': 'college_ypr_rank', 'Breakout Age': 'breakout_age',
                      'College Target Share': 'college_target_share', 'Breakout Age Rank': 'breakout_age_rank',
                      'College Dominator Rating': 'college_dominator_rating'}

        for k,v in cp_mapping.items():
            if cp.has_key(k):
                player[v] = cp.get(k)

        # Core
        core = data['Core']
        core_mapping = {'ADP': 'adp', 'ADP Trend': 'adp_trend', 'ADP Year': 'adp_year', 'Height': 'height',
                   'Height (Inches)': 'height_inches', 'Weight': 'weight', 'Weight Raw': 'weight_raw', 'BMI': 'bmi',
                   'BMI Rank': 'bmi_rank', 'Hand Size': 'hand_size', 'Hand Size Rank': 'hand_size_rank',
                   'Arm Length': 'arm_length', 'Arm Length Rank': 'arm_length_rank', 'College': 'college',
                   'Draft Year': 'draft_year', 'Draft Pick': 'draft_pick', 'Birth Date': 'birth_date', 'Age': 'age',
                   'Quality Score': 'quality_score', 'Quality Score Rank': 'quality_score_rank', 'Position': 'position'}

        for k,v in core_mapping.items():
            if core.has_key(k):
                player[v] = core.get(k)

        ## Core: nested data
        player['site_team_name'] = core['Team']['Name']
        player['site_team_id'] = core['Team']['Team_ID']
        player['best_comparable'] = core['Best Comparable Player']['Player_ID']

        # Game Logs


        # Medical History


        # Performance Metrics


        # Workout Metrics

        return player

    def players(self, content):
        '''
        Parses list of players, with ids, from playerprofiler
        '''
        try:
            data = json.loads(content)

        except Exception as e:
            data = None
            logging.exception('could not load content: {}'.format(e))

        if data:
            return [{'site': 'playerprofiler', 'site_player_name': p.get('Full Name'), 'site_player_id': p.get('Player_ID')} for p in data['data']['Players']]
        else:
            return None

    def rankings(self, content, ranking_type=None):
        '''
        Parses current season, dynasty, and weekly rankings from playerprofiler
        '''
        rankings = []
        ts = datetime.datetime.now('America/Chicago')

        try:
            p = json.loads(content)

        except Exception as e:
            p = None
            logging.exception('could not load content: {}'.format(e))

        positions = ['QB', 'RB', 'WR', 'TE']
        rtypes = ['Dynasty', 'Rookie', 'Seasonal', 'Weekly']

        if p:
            if ranking_type == 'dynasty':
                pass

            elif ranking_type == 'rookie':
                pass

            elif ranking_type == 'seasonal':
                pass

            elif ranking_type == 'weekly':
                pass

            else:
                rankings = p['data']
                for rt in rtypes:
                    for pos in positions:
                        node = rankings[rt][pos]

        else:
            return None

if __name__ == '__main__':
    # can use as test
    #with open('/home/sansbacon/players.json', 'r') as infile:
    #    p = PlayerProfilerNFLParser()
    #    print(p.players(infile.read()))

    with open('/home/sansbacon/player.json', 'r') as infile:
        p = PlayerProfilerNFLParser()
        pprint.pprint(p.player_page(infile.read()))

    with open('/home/sansbacon/receiver.json', 'r') as infile:
        p = PlayerProfilerNFLParser()
        pprint.pprint(p.player_page(infile.read()))

    with open('/home/sansbacon/te.json', 'r') as infile:
        p = PlayerProfilerNFLParser()
        pprint.pprint(p.player_page(infile.read()))

#pass
