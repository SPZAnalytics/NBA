# -*- coding: utf-8 -*-
# playerxref.py
# provides cross-reference of players between sites

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

<<<<<<< HEAD
from nfl.db import nflpg
=======
from nfl.db import nflpg.NFLPostgres
>>>>>>> ace1da00fd9afc9f38280055e9751ec1562994bb

class NFLPlayerXRef(object):

    def __init__(self, database, user, password):
    
<<<<<<< HEAD
        self.nflp = nflpg.NFLPostgres(database, user, password)
=======
        self.nflp = NFLPostgres(database, user, password)
>>>>>>> ace1da00fd9afc9f38280055e9751ec1562994bb
        
    def draftkings(self):
        '''
        Matches draftkings playernames to player_id in player table
        '''
        players_tbl = {}                                  
                      
        for player in self.nflp.select_dict('SELECT * FROM player'):
            pkey = '{} {}_{}'
            first, last = player.get('name', ' , ').split(', ')[0:2]
            if first and last:
                pos = player.get('position')
                players_tbl[pkey.format(last, first, pos)] = player
                
        matches = []
        for player in fixed:
            key = '{}_{}'.format(player.get('Name'), player.get('Position'))           
            try:
                pid = players_tbl[key]['player_id']
                match = {}       
                match['player_id'] = pid
                match['site'] = 'dk'  
                match['site_player_id'] = key 
                match['site_player_name'] = player.get('Name')          
                match['site_player_position'] = player.get('Position')
                matches.append(match)
            except:
                next
                
        return matches
    
    def ffanalytics(self):
        '''
        Matches ffanalytics playernames to player_id in player table
        '''

        matches = []

        for ffa in ffa_players:                                

            try:
                first, last = ffa.get('playername').split(' ')[0:2]
                pos = ffa.get('position')
                pkey = '{}_{}_{}'.format(last, first, pos)
            except:
                next
                                                        
            try:
                pid = players_tbl[pkey]['player_id']
            except:
                next
                 
            match = {}
                                     
            match['player_id'] = pid
            match['site'] = 'ffanalytics'  
                                   
            spid = ffa.get('playerId')     
            if not spid: next              
            match['site_player_id'] = spid 
                                       
            dname = ffa.get('playername')   
            if not dname: next               
            match['site_player_name'] = dname          
                                                            
            match['site_player_team'] = ffa.get('team')        
            match['site_player_position'] = ffa.get('position')
                              
            matches.append(match)
        
        return matches
        
    def footballoutsiders(self):
        '''
        Matches footballoutsiders key to player_id in player table
        '''
        players_tbl = {}                                  
                      
        for player in nflp.select_dict('SELECT * FROM player'):
            pkey = '{} {}|{}|{}'
            first, last = player.get('name', ' , ').split(', ')[0:2]
            if first and last:
                pos = player.get('position')
                team = player.get('team')
                players_tbl[pkey.format(first, last, pos, team)] = player

        matches = []

        for fo in fo_players:                                

            try:
                pid = players_tbl[fo.get('Key')]['player_id']
            except:
                next
                 
            match = {}
                                     
            match['player_id'] = pid
            match['site'] = 'footballoutsiders'  
                                   
            spid = fo.get('FO ID')     
            if not spid: next              
            match['site_player_id'] = spid 
                                       
            dname = fo.get('Player')   
            if not dname: next               
            match['site_player_name'] = dname          
                                                            
            match['site_player_team'] = fo.get('Team')        
            match['site_player_position'] = fo.get('POS')
                              
            matches.append(match)
    
        return matches
