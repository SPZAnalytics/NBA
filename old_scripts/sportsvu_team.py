#!/usr/bin/env python3.5
#Author : Benika Hall
#Email : Benika.Hall@gmail.com


from urllib.request import *
import urllib.request, json, sys, requests
import pymongo

url = "http://api.probasketballapi.com/sportsvu/team"

#api_key = "EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv"
#query_string = {'api_key':'EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv','team_id':'1610612765','season':'2015'}



#print(r.text)


f = open('team_ids.txt', 'r')
ids = f.readlines()

for i in ids:
	query_string = {'api_key':'EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv','team_id':[i],'season':'2015'}
	r = requests.post(url, data=query_string)
	json_data = json.loads(r.text) #Convert JSON into Python readable object
	print(r.text)

#Get a specific advanced stats 


#for j in json_data:
	#print(j['team_id'], j['off_rating'], j['ast_pct'])
