The flex csv file is messed up, so want to use HTML page instead

### headers

season
week
scoring_format

overall_rank
site_player_id
site_player_name
team
player_status
pos_rank
opp
best
worst
avg
stdev

###  body

table id=data
tr class ~ mpb-player

#data > tbody > tr.mpb-player-9808.mpb-taken

<tr class="mpb-player-9808 mpb-taken"><td>1</td>
<td class="player-label"><a href="/nfl/players/antonio-brown.php?type=flex&amp;scoring=PPR&amp;week=3">Antonio Brown</a> <small class="grey">PIT</small> <a href="#" class="fp-player-link fp-id-9808" fp-player-name="Antonio Brown"></a><div class=" fpNewsPlayer"><a class=" fpIcon fpNewsIconInfo" href="javascript:void(0);" title="View Player Card" data-fp-id="9808" data-fp-icon="{&quot;sport&quot;:&quot;nfl&quot;,&quot;fpId&quot;:&quot;9808&quot;}" id="fp_icon0" onclick="playercardGenerator.openNewsPopup(event, JSON.parse(this.getAttribute('data-fp-icon')));return false;"></a></div></td>
<td>WR1</td>
<td>  at  PHI</td>
<td>1</td>
<td>18</td>
<td>1.5</td>
<td>1.9</td>
</tr>

from collections import deque
import logging
import re

from bs4 import BeautifulSoup


with open('/home/sansbacon/flex.html', 'r') as infile:
	soup = BeautifulSoup(infile.read(), 'lxml')

def weekly_flex_rankings(content, season, week, scoring_type):
	tbody = soup.find('table', {'id': 'data'}).find('tbody')

	players = []

	for tr in tbody.find_all('tr'):
		player = {'site': 'fantasypros', 'season': season, 'week': week, 'scoring_type': scoring_type, 'ranking_type': 'flex'}
		a = tr.find('a', {'href': re.compile(r'/nfl/players')})
		if a:
			player['site_player_name'] = a.text.strip()  
			
		cls = tr.get('class')
		if cls and len(cls) > 0:
			player['site_player_id'] = cls[0].split('-')[-1]
			
		tds = deque(tr.find_all('td'))
		if tds and len(tds) == 8:
			player['flex_rank'] = tds.popleft().text.strip()
			player['team'] = tds.popleft().find('small').text.strip()
			player['position_rank'] = tds.popleft().text.strip()
			player['opp'] = tds.popleft().text.strip()
			player['best'] = tds.popleft().text.strip()
			player['worst'] = tds.popleft().text.strip()
			player['avg'] = tds.popleft().text.strip()
			player['stdev'] = tds.popleft().text.strip()
			players.append(player)
	
	return players
