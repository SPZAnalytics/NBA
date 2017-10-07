import urllib, json, requests

url_1='http://api.probasketballapi.com/sportsvu/player'
api_key='EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv'

#query_string = 'api_key='+ api_key + '&season=2015'
query = {'api_key': 'my_api_key', 'season': '2015', 'team_id' : 'Cle'}
r = requests.post(url_1, data=query)
print(r)
#r = requests.post(url_1, data=query_string)

