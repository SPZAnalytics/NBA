#!/usr/bin/env python3.5
#Author : Benika Hall
#Email : Benika.Hall@gmail.com

from urllib.request import *
import urllib.request, json, sys, requests
import pymongo

url="http://api.probasketballapi.com/four_factor/team"

#api_key = "EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv"
#query_string = {'api_key':'EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv','team_id':'1610612765','season':'2015'}
#print(r.text)

f = open('team_ids.txt', 'r')
ids = f.readlines()

for i in ids:
	query_string = {'api_key':'EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv','team_id':[i],'season':'2015'}
	r = requests.post(url, data=query_string)
	json_data = json.loads(r.text)  #Convert JSON into Python readable object
	print(r.text)
	#for j in json_data: # Use thisif you want to print certain stats
		#print(j['team_id'], j['period'], j['opponent_id'], j['opp_tov_pct'], j['tm_tov_pct'])

	#print(r.text)

#f2= open('four_factors_team_stats.json', 'w')
#f2.write(r.text)
#f2.close()


