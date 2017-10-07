import urllib
import simplejson
 
response = urllib.urlopen("http://stats.nba.com/js/data/sportvu/catchShootData.js")
data = simplejson.load(response)
print(data)
