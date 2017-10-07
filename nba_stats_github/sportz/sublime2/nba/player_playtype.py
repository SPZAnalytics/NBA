#!/usr/bin/env python3.5
#Author : Benika Hall
#Email : Benika.Hall@gmail.com


from urllib.request import *
import urllib.request, json, sys, requests
import pymongo


player_transition= "http://stats.nba.com/js/data/playtype/player_Transition.js"
player_isolation= "http://stats.nba.com/js/data/playtype/player_Isolation.js"
player_ball_handler = "http://stats.nba.com/js/data/playtype/player_PRBallHandler.js"
player_post_up = "http://stats.nba.com/js/data/playtype/player_Postup.js"
player_hand_off = "http://stats.nba.com/js/data/playtype/player_Handoff.js"
player_cut = "http://stats.nba.com/js/data/playtype/player_Cut.js"
player_putbacks = "http://stats.nba.com/js/data/playtype/player_OffRebound.js"
player_roll_man = "http://stats.nba.com/js/data/playtype/player_PRRollman.js"

transition = requests.post(player_transition)
f1 = open('player_transition.json','w')
f1.write(transition.text)
f1.close()
isolation = requests.post(player_isolation)
f2 = open('player_isolation.json','w')
f2.write(isolation.text)
f2.close()
ball_handler = requests.post(player_ball_handler)
f3 = open('player_ball_handler.json','w')
f3.write(ball_handler.text)
f3.close()
post_up = requests.post(player_post_up)
f4 = open('player_post_up.json','w')
f4.write(post_up.text)
f4.close()
cut = requests.post(player_cut)
f5 = open('player_cut.json','w')
f5.write(cut.text)
f5.close()
handoff = requests.post(player_hand_off)
f6 = open('player_handoff.json','w')
f6.write(handoff.text)
f6.close()
putbacks = requests.post(player_putbacks)
f7 = open('player_putbacks.json','w')
f7.write(putbacks.text)
f7.close()
roll_man = requests.post(player_roll_man)
f8 = open('player_roll_man.json','w')
f8.write(roll_man.text)
f8.close()
