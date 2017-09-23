#!/usr/bin/env python3.5
from urllib.request import *
import urllib.request, json, sys, requests
import pymongo

url = "https://probasketballapi.com/stats/players"
api_key = "EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv"
query_string = {'api_key':'EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv','season':'2015'}

r = requests.post(url, data=query_string)

#print(r.text)
f = open('player_info.json', 'w')
f.write(r.text)
f.close()

json_data = json.loads(r.text)
for i in json_data:
	print(i['player_id'], i['team_id'])#, i['player_name'])#, i['last_name'])
