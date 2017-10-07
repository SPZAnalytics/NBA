import copy
import json
import logging
import os
import pprint
import time

import browsercookie
from bs4 import BeautifulSoup
import requests
import requests_cache


def _get(url):
    '''
    Generic method to get resource with cookies / error handling
    
    Arguments:
        url(str): url of resource
        
    Returns:
        response
    '''
    try:
        response = s.get(url, cookies = cj)
        response.raise_for_status()

    except requests.HTTPError:
        logging.exception('could not fetch {0}'.format(url))

    return response
    
def _parse(response, cols, extras):
    '''
    Generic method to create dictionary from response
    
    Arguments:
        response(requests.response): response from requests.get
        cols(list): keys for dictionary
    '''
    
    dicts = []
    
    try:
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table', {'id': 'dataTable'})
        trs = table.findAll('tr')

        for tr in trs[1:]:
            vals = [td.text.replace('%', '') for td in tr.findAll('td')]
            combined = dict(zip(cols, vals))
            
            for k,v in extras.items(): 
                combined[k] = v
            
            dicts.append(combined)
        
    except Exception, e:
        logging.exception('error in processing response: {}'.format(e))

    return dicts
    
def home_road_dvoa(years, teams, sides=['o', 'd']):
    '''
    NEED TO UPDATE
    '''
    base_url = 'http://www.footballoutsiders.com/premium/homeRoadDvoa.php?od={od}&year={y}&team={t}&week={w}'
    cols = ['team', 'home_dvoa', 'home_rank', 'road_dvoa', 'road_rank', 'total_dvoa', 'total_rank']
    hrDvoa = []

    for year in years:
        for team in teams:
            for side in sides:
                url = base_url.format(y=year, w=week, t=team, od=side)

                try:
                    filename = 'homeRoadDVOA-{y}_{w}_{t}.json'.format(y=year, w=week, t=team)
                    response = s.get(url, cookies = cj)
                    response.raise_for_status()
                    
                except requests.HTTPError:
                    print 'could not fetch {0}'.format(url)

                finally:
                    time.sleep(.5)
                    
                if response.content:
                    try:
                        soup = BeautifulSoup(response.content, 'lxml')
                        table = soup.find('table', {'id': 'dataTable'})
                        trs = table.findAll('tr')

                        teamDvoa = []

                        for tr in trs[1:]:
                            vals = [td.text for td in tr.findAll('td')]
                            teamWeekDvoa = dict(zip(cols, vals))
                            teamWeekDvoa['season'] = year
                            teamWeekDvoa['team'] = team
                            teamDvoa.append(teamWeekDvoa)
                        
                        hrDvoa += teamDvoa

                        with open(os.path.join(dldir, filename), 'w') as outfile:
                            json.dump(teamDvoa, outfile)               
                    
                    except Exception, e:
                        print 'error in processing response: {}'.format(e)

    return hrDvoa

def one_team_line_yards(teams, sides=['o', 'd']):
    '''
    NEED TO UPDATE
    '''
    otly = []
    base_url = 'http://www.footballoutsiders.com/premium/oneTeamLineYards?od={od}&year={y}&team={t}&week=1'
    cols = ['year', 'adj_line_yds', 'adj_line_yds_rank', 'rb_yds', 'rb_yds_rank', 'power_success', 'power_success_rank', 'power_success_nfl_avg', 'open_field_yds', 'open_field_yds_rank', 'open_field_yds_nfl_avg', 'sec_level', 'sec_level_rank', 'sec_level_nfl_avg', 'stuffed', 'stuffed_rank', 'stuffed_nfl_avg', 'adj_sack_rate', 'adj_sack_rate_rank', 'adj_sack_rate_sacks']

    for team in teams:
        for side in sides:
            url = base_url.format(y=year, t=team, od=side)

            try:
                filename = 'otly-{t}_{s}.json'.format(s=side, t=team)
                response = s.get(url, cookies = cj)
                response.raise_for_status()
                
            except requests.HTTPError:
                print 'could not fetch {0}'.format(url)

            finally:
                if response.from_cache:
                    print 'got from cache'
                else:
                    time.sleep(.5)
                
            if response.content:
                try:
                    soup = BeautifulSoup(response.content, 'lxml')
                    table = soup.find('table', {'id': 'dataTable'})
                    trs = table.findAll('tr')
        
                    for tr in trs[1:]:
                        vals = [td.text.replace('%', '') for td in tr.findAll('td')]
                        t = dict(zip(cols, vals))
                        t['team'] = team
                        t['side'] = side
                        otly.append(t)

                except Exception, e:
                    print 'error in processing response: {}'.format(e)

    return otly

def weekByTeam(year, team, pause=1):
    '''
    Weekly DVOA by team by season
    
    Argument: 
        year(int)
        team(str)
        
    '''
    base_url = 'http://www.footballoutsiders.com/premium/weekByTeam.php?year={y}&team={t}&od=O&week=1'
    cols = ['week', 'opponent', 'total_dvoa', 'off_dvoa', 'off_pass_dvoa', 'off_rush_dvoa',
            'def_dvoa', 'def_pass_dvoa', 'def_rush_dvoa', 'st_dvoa']
 
    url = base_url.format(y=year, t=team)
    response = _get(url)
    extras = {'season': int(year), 'team': team}

    if not response.from_cache:
        time.sleep(pause)           
    
    if response.content:
        return _parse(response, cols, extras)
    else:
        return None
    
def weekTeamSeasonDvoa(year, week, pause=1):
    '''
    Weekly DVOA by team - includes ranks and weightings
    
    Argument: 
        year(int)
        week(int)
        
    '''
    base_url = 'http://www.footballoutsiders.com/premium/weekTeamSeasonDvoa.php?od=O&team=ARI&year={y}&week={w}'
    cols = ['team', 'wl', 'total_dvoa', 'total_dvoa_rank', 'weighted_dvoa', 'weighted_dvoa_rank', 'off_dvoa', 'off_dvoa_rank',
            'weighted_off_dvoa', 'weighted_off_dvoa_rank', 'def_dvoa', 'def_dvoa_rank', 'weighted_def_dvoa', 'weighted_def_dvoa_rank',
             'st_dvoa', 'st_dvoa_rank', 'weighted_st_dvoa', 'weighted_st_dvoa_rank']
    url = base_url.format(y=year, w=week)
    response = _get(url)
    extras = {'season': int(year), 'week': int(week)}

    if not response.from_cache:
        time.sleep(pause)
    
    if response.content:
        teams = _parse(response, cols, extras)
        
        for idx, team in enumerate(teams):
            wl = team.get('wl')
            
            if wl:
                teams[idx]['w'], teams[idx]['l'] = wl.split('-')
                
        return teams

    else:
        return None

def weekly_dvoa(years, weeks, teams):
    ''' need to merge 2 resources:
            weekTeamSeasonDvoa
            weekByTeam
    '''
    
    results = []
    
    for year in years:
        logging.debug(year)
        wtsds = []
        wbts = []
        combined = []
        
        for week in weeks:
            logging.debug(week)
            wtsds += weekTeamSeasonDvoa(year, week)
            
        for team in teams:
            logging.debug(team)
            wbts += weekByTeam(year, team)
        
        # combine results
        for wtsd in wtsds:
            for wbt in wbts:
                if (int(wtsd['season']) == int(wbt['season']) and wtsd['team'] == wbt['team'] and int(wtsd['week']) == int(wbt['week'])):
                    z = wtsd.copy()
                    z.update(wbt)
                    results.append(z)

    return results

if __name__ == '__main__':    
    requests_cache.install_cache('fbo-api_cache')
    cj = browsercookie.chrome()
    s = requests.Session()

    dldir = os.path.join(os.path.expanduser('~'), 'pfr-api')

    years = range(2000,2016)
    weeks = range(1,18)
    teams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAC', 'KC', 'MIA', 'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'OAK', 'PHI', 'PIT', 'SD', 'SEA', 'SF', 'STL', 'TB', 'TEN', 'WAS']
    
    otly = one_team_line_yards(teams, sides=['o', 'd'])
    with open(os.path.join(dldir,'otly.json'), 'w') as outfile:
        json.dump(otly, outfile)


    #cols = ['week', 'opponent', 'total_dvoa', 'off_dvoa', 'off_pass_dvoa', 'off_rush_dvoa',
    #'def_dvoa', 'def_pass_dvoa', 'def_rush_dvoa', 'st_dvoa']

    #teamDvoas = week_by_team(dldir=dldir, years=years, teams=teams)
    
    #with open(os.path.join(dldir,'teamDvoas.json'), 'w') as outfile:
    #    json.dump(teamDvoas, outfile)
    
