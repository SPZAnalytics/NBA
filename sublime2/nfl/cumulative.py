#!/usr/bin/env python3.5
#Author : Benika Hall
#Email : Benika.Hall@gmail.com


from urllib.request import *
import urllib.request, json, sys, requests, base64
import pymongo, base64string

request = urllib2.Request("https://www.mysportsfeeds.com/api/feed/pull/nfl/{(2015)-(2016)-regular}/cumulative_player_stats.{json}")
base64string = base64.encodestring('%s:%s' % (username, password).replace('\n', '')
request.add_header('Authorization', b'Basic' + base64.b64encode(benikah + b':' + CHamps___2015))  
result = urllib2.urlopen(request)

url = "https://www.mysportsfeeds.com/api/feed/pull/nfl/{(2015)-(2016)-regular}/cumulative_player_stats.{json}"#?playerstats={player-stats}"

r = requests.post(url)
#json_data = json.loads(r.text) #Convert JSON into Python readable object
print(result.text)
