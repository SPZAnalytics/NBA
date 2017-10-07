from random import sample

def multi_entry(players, n, group_size, team_exclude, team_exclude_pool, player_exclude, player_exclude_pool, projection_formula='tournament', randomize_projections=True, ownership_penalty=False):

	lineups = []

	for i in range(1, int(n/group_size) + 1):
		pexcl = player_exclude + sample(player_exclude_pool, int(len(player_exclude_pool)/4) + 1)
		texcl = team_exclude + sample(team_exclude_pool, int(len(team_exclude_pool)/3) + 1)
		l = a.optimize(players, n=group_size, projection_formula=projection_formula, team_exclude=texcl, player_exclude=pexcl, randomize_projections=True)
		lineups.append(l)

	lineups = [item for sublist in lineups for item in sublist]
	return [item for sublist in lineups for item in sublist]
	
if __name__ == '__main__':
	player_exclude = []
	team_exclude = []
	player_exclude_pool = ['T.Y. Hilton', 'Mohamed Sanu', 'Jermaine Gresham', 'Minnesota Defense', 'Kenneth Farrow', 'Aldrick Robinson', 'Devonta Freeman', 'David Johnson', "Le'Veon Bell", 
						   'Jordy Nelson', 'Sam Bradford', 'Tyrod Taylor', 'Jordan Matthews', 'Demaryius Thomas', 'NY Giants Defense', 'Philadelphia Defense', 'Baltimore Defense', 'New England Defense'] 
	team_exclude_pool = ['KC', 'TEN', 'CHI', 'GB', 'BAL', 'PHI', 'PIT', 'SF', 'NO', 'CLE', 'ARI', 'MIN', 'DEN', 'NE']
