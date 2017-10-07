

import multiprocessing
import pickle

from joblib import Parallel, delayed  
import numpy as np
import pandas as pd

class NBASim(object):
    '''
    Usage:
        import pandas as pd
        from NBASim import NBASim
        
        sim = NBASim()
        urn = 'http://www.dougstats.com/15-16RD.txt'
        frame = pd.read_fwf(urn)
        results = sim.sim(frame, iterations=10000)
        sim.to_csv(results, 'sim.csv')
    '''
        

    def _nbasim(self, frame, i, n, prange, tid_range, value_columns, rank_columns):

        # take random sample of players
        np.random.seed()
        players = frame.ix[np.random.choice(frame['pid'], n)]
        players['team_id'] = tid_range

        # team totals
        team_totals = pd.pivot_table(players, index=['team_id'], values=value_columns)

        # adjustments
        team_totals['FGP'] = team_totals['FGM'] / team_totals['FGA'] 
        team_totals['FTP'] = team_totals['FTM'] / team_totals['FTA'] 
        
        # team ranks
        team_ranks = pd.DataFrame({col:team_totals[col].rank(ascending=1) for col in rank_columns})
        team_ranks['sim_id'] = i
        team_ranks['team_id'] = prange
        team_ranks['TOT'] = team_ranks[rank_columns].sum(axis=1)

        # add to results dictionary, key is the iteration number
        return pd.merge(left=players.loc[:,['Player', 'team_id']], right=team_ranks, how='left', left_on='team_id', right_on='team_id')


    def _nbasim_opt(self, frame, i, n, num_teams, team_ids, prange, value_columns, rank_columns):

        frame['team_id'] = np.random.shuffle(team_ids)

        # team totals
        team_totals = pd.pivot_table(frame[frame['team_id'] <= num_teams], index=['team_id'], values=value_columns)

        # adjustments
        team_totals['FGP'] = team_totals['FGM'] / team_totals['FGA']
        team_totals['FTP'] = team_totals['FTM'] / team_totals['FTA']

        # team ranks
        team_ranks = pd.DataFrame({col:team_totals[col].rank(ascending=1) for col in rank_columns})
        team_ranks['sim_id'] = i
        team_ranks['TOT'] = team_ranks[rank_columns].sum(axis=1)

        # add to results dictionary, key is the iteration number
        return pd.merge(left=frame.loc[:,['Player', 'team_id']], right=team_ranks, how='left', left_on='team_id', right_on='team_id')


    def sim(self, frame, iterations=500, num_players = 10, num_teams = 10):

        # adjustments ahead of time
        frame = frame[frame.Min >= 250]
        pool_size = len(frame.index)
        num_groups, remainder= divmod(pool_size, num_teams)
        tids = (num_groups + 1) * list(range(1, 11))
        frame['team_id'] = 0
        frame['pid'] = list(range(1, pool_size + 1))
        frame['TO'] = 0 - frame['TO']

        n = num_teams * num_players
        value_columns = ['FGM', 'FGA', 'FTM', 'FTA', '3M', 'TR', 'AS', 'ST', 'BK', 'PTS', 'TO']
        rank_columns = ['FGP', 'FTP', '3M', 'TR', 'AS', 'ST', 'BK', 'PTS', 'TO']

        # parallelize
        #results = Parallel(n_jobs=num_cores)(delayed(self._nbasim)(frame, i, n, prange, tid_range, value_columns, rank_columns) for i in xrange(1, iterations+1))
        results = self._nbasim_opt(frame=frame, i=0, n=n, num_teams=num_teams, team_ids=tids[0:pool_size],
                                   prange=list(range(0, num_players)), value_columns=value_columns, rank_columns=rank_columns)
        players = results
        #players = pd.concat(results)
        players['VORP'] = players['TOT'] - players['TOT'].mean()
        return (players.loc[:,['Player', 'TOT', 'VORP']].groupby('Player').mean().sort('VORP', ascending=False))
        
if __name__ == '__main__':
    sim = NBASim()
    frame = pd.read_fwf('http://www.dougstats.com/15-16RD.txt')
    print(sim.sim(frame, iterations=20))