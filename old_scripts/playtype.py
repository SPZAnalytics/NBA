#!/usr/bin/env python3.5
#Author : Benika Hall
#Email : Benika.Hall@gmail.com


from urllib.request import *
import urllib.request, json, sys, requests
import pymongo


team_transition= "http://stats.nba.com/js/data/playtype/team_Transition.js"
team_isolation= "http://stats.nba.com/js/data/playtype/team_Isolation.js"
team_ball_handler = "http://stats.nba.com/js/data/playtype/team_PRBallHandler.js"
team_post_up = "http://stats.nba.com/js/data/playtype/team_Postup.js"
team_hand_off = "http://stats.nba.com/js/data/playtype/team_Handoff.js"
team_cut = "http://stats.nba.com/js/data/playtype/team_Cut.js"
team_putbacks = "http://stats.nba.com/js/data/playtype/team_OffRebound.js"
team_roll_man = "http://stats.nba.com/js/data/playtype/team_PRRollman.js"

transition = requests.post(team_transition)
f1 = open('transition.json','w')
f1.write(transition.text)
f1.close()
isolation = requests.post(team_isolation)
f2 = open('team_isolation.json','w')
f2.write(isolation.text)
f2.close()
ball_handler = requests.post(team_ball_handler)
f3 = open('team_ball_handler.json','w')
f3.write(ball_handler.text)
f3.close()
post_up = requests.post(team_post_up)
f4 = open('team_post_up.json','w')
f4.write(post_up.text)
f4.close()
cut = requests.post(team_cut)
f5 = open('team_cut.json','w')
f5.write(cut.text)
f5.close()
handoff = requests.post(team_hand_off)
f6 = open('tteam_handoff.json','w')
f6.write(handoff.text)
f6.close()
putbacks = requests.post(team_putbacks)
f7 = open('team_putbacks.json','w')
f7.write(putbacks.text)
f7.close()
roll_man = requests.post(team_roll_man)
f8 = open('team_roll_man.json','w')
f8.write(roll_man.text)
f8.close()
