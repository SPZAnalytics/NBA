#!/usr/bin/env python3.5

from urllib.request import *
import urllib.request, json, sys, requests
import pymongo

url = 'http://api.probasketballapi.com/player'
#api_key = "EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv"
query_string = {'api_key':'EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv'}

r = requests.post(url, data=query_string)

#print(r.text)
f = open('player_info.json', 'w')
f.write(r.text)
f.close()

json_data = json.loads(r.text)
for i in json_data:
	print(i['id'])#, i['position'],i['player_name'])# i['first_name'], i['last_name'])


