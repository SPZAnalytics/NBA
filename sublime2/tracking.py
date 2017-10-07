#!/usr/bin/env python3.5
#Author : Benika Hall
#Email : Benika.Hall@gmail.com


from urllib.request import *
import urllib.request, json, sys, requests
import pymongo


#league_tracking = "http://stats.nba.com/stats/leaguedashptstats'
pullup_address = "http://stats.nba.com/js/data/sportvu/pullUpShootData.js" 
drives_address = "http://stats.nba.com/js/data/sportvu/drivesData.js" 
defense_address = "http://stats.nba.com/js/data/sportvu/defenseData.js" 
passing_address = "http://stats.nba.com/js/data/sportvu/passingData.js"
touches_address = "http://stats.nba.com/js/data/sportvu/touchesData.js" 
speed_address = "http://stats.nba.com/js/data/sportvu/speedData.js"
rebounding_address = "http://stats.nba.com/js/data/sportvu/reboundingData.js"
catchshoot_address = "http://stats.nba.com/js/data/sportvu/catchShootData.js" 
shooting_address = "http://stats.nba.com/js/data/sportvu/shootingData.js"

r = requests.post(league_tracking)
#json_data = json.loads(r.text) #Convert JSON into Python readable object
print(r.text)
