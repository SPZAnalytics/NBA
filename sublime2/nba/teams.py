#!/usr/bin/env python3.5
#Author : Benika Hall
#Email : Benika.Hall@gmail.com

from urllib.request import *
import urllib.request, json, sys, requests
import pymongo

url = "http://api.probasketballapi.com/team"
api_key = "EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv"
query_string = {'api_key':'EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv'}
r = requests.post(url, data=query_string)

f = open('team_info.json', 'w')
f.write(r.text)
f.close()


json_data = json.loads(r.text) #Convert JSON into Python readable object
for i in json_data:
	print(i['id'], i['abbreviation'])
	
