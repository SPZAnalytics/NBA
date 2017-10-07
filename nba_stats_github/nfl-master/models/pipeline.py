# coding: utf-8
import pickle

import pandas as pd
from sklearn.model_selection import train_test_split
from tpot import TPOTClassifier

from nfl.parsers.fantasylabs import FantasyLabsNFLParser


with open('/home/sansbacon/models.pkl', 'rb') as infile:
    models = pickle.load(infile)

p = FantasyLabsNFLParser()

dataset = []
for year, yearmodels in models.items():
    for week, weekmodel in yearmodels.items():
        dataset.append(p.model(weekmodel, site='dk'))
    
df = pd.DataFrame([item for sublist in dataset for item in sublist])
# need to create feature from InjuryStatus
# 'InjuryStatus'

common_features = ['AvgPts', 'Ceiling', 'CeilingPct', 'Consistency', 'Floor', 'FloorPct', 'ImpPts', 'OppPlusMinusPct', 'Plus_Minus', 'ProjPlusMinusPct', 'Score', 'Season_PPG', 'Season_Plus_Minus', 'Upside', 'Vegas']
qb_features = common_features + ['AdjYPA', 'PassINTPct', 'PassSackPct', 'PassTDPct', 'PassingSuccessfulPct', 'YardsPerPassingAttempt']
rb_features = common_features + ['MktShrPct', 'OffensiveSnapsMarketShare', 'OpportunitiesRedZone', 'OpportunitiesRedZone10', 'OpportunitiesRedZone5', 'RedZoneSnaps', 'RedZoneSnaps10', 'RedZoneSnaps5', 'RedZoneTouchdownPct', 'RushingFantasyPct', 'RushingSuccessfulAllowedPct',  'RushingSuccessfulPct', 'RushingSuccessfulPctRedZone', 'RushingTouchdownsMarketShare', 'RushingTouchdownsRedZonePct', 'RushingYardsMarketShare']
wr_features = common_features + ['MktShrPct', 'OffensiveSnapsMarketShare', 'OpportunitiesRedZone', 'OpportunitiesRedZone10', 'OpportunitiesRedZone5', 'RedZoneSnaps', 'RedZoneSnaps10', 'RedZoneSnaps5', 'RedZoneTouchdownPct', 'ReceivingTargetsMarketShare', 'ReceivingTouchdownsMarketShare', 'ReceivingTouchdownsRedZonePct', 'ReceivingYardsMarketShare']
te_features = common_features + ['MktShrPct', 'OffensiveSnapsMarketShare', 'OpportunitiesRedZone', 'OpportunitiesRedZone10', 'OpportunitiesRedZone5', 'RedZoneSnaps', 'RedZoneSnaps10', 'RedZoneSnaps5', 'RedZoneTouchdownPct', 'ReceivingTargetsMarketShare', 'ReceivingTouchdownsMarketShare', 'ReceivingTouchdownsRedZonePct', 'ReceivingYardsMarketShare']

#df['x3'] = df.ActualPoints * 1000 / df.Salary > 3
#df['x4'] = df.ActualPoints * 1000 / df.Salary > 4

qb = df[(df.Position == 'QB') & (df.AvgPts >= 12)]
rb = df[(df.Position == 'RB') & (df.AvgPts >= 8)]
wr = df[(df.Position == 'WR') & (df.AvgPts >= 8)]
te = df[(df.Position == 'TE') & (df.AvgPts >= 6)]

# need to remove nulls, but x3 is not null, so remove, then split off
X = qb[qb_features + ['x3']]
X = X[-X.isnull().any(axis=1)]
y = X['x3']
X.drop('x3', axis=1)

print('start qb model\n\n')
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, test_size=0.25)
tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2)
tpot.fit(X_train, y_train)
print('qb model: {}'.format(tpot.score(X_test, y_test)))
print('\n\n')

X = rb[rb_features]
y = rb['x3']

print('start rb model\n\n')
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, test_size=0.25)
tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2)
tpot.fit(X_train, y_train)
print('rb model: {}'.format(tpot.score(X_test, y_test)))

X = wr[wr_features]
y = wr['x3']

print('start wr model\n\n')
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, test_size=0.25)
tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2)
tpot.fit(X_train, y_train)
print('wr model: {}'.format(tpot.score(X_test, y_test)))

X = te[te_features]
y = te['x3']

print('start te model\n\n')
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, test_size=0.25)
tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2)
tpot.fit(X_train, y_train)
print('te model: {}'.format(tpot.score(X_test, y_test)))
