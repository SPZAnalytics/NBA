import logging
from operator import add
from random import randint, random, shuffle, uniform

from numba import jit


class Player(object):
    def __init__(self, name, team, oppos, position, salary, projection):
        self.self = self
        self.name = name
        self.team = team
        self.opp = oppos
        self.position = position
        self.salary = salary
        self.points = projection

    def __iter__(self):
        return iter(self.list)

    def __str__(self):
        return "{} {} {} {}".format(self.name ,self.position ,self.salary, self.points)


class GenAlg(object):

    def __init__(self, players=[], pool={}, positions=['qb', 'rb', 'wr', 'te', 'flex', 'dst']):
        self.players = players
        self.pool = pool
        self.positions = positions
        self._qbs = []
        self._rbs = []
        self._wrs = []
        self._tes = []
        self._dsts = []
        self._flexs = []

    @property
    def qbs(self):
        if not self._qbs:
            self._qbs = [player for player in self.players if player.position == 'QB' and player.points >= 16]
        return self._qbs

    @property
    def rbs(self):
        if not self._rbs:
            self._rbs = [player for player in self.players if player.position == 'RB' and player.points >= 9]
        return self._rbs

    @property
    def wrs(self):
        if not self._wrs:
            self._wrs = [player for player in self.players if player.position == 'WR' and player.points >=9]
        return self._wrs

    @property
    def tes(self):
        if not self._tes:
            self._tes = [player for player in self.players if player.position == 'TE' and player.points >= 7]
        return self._tes

    @property
    def dsts(self):
        if not self._dsts:
            self._dsts = [player for player in self.players if player.position == 'DST' and player.points >= 6]
        return self._dsts

    @property
    def flexs(self):
        if not self._flexs:
            self._flexs = [player for player in self.players if player.position != 'QB' and player.position != 'DST' and player.points >= 8]
        return self._flexs

    def CreatePopulation(self, count):
        return [self.CreateRandomTeam() for i in range(0, count)]

    @jit
    def choice(self, seq):
        '''
        Use for numba compatibility - does not support choice or sample

        Returns:

        '''
        return seq[randint(0, len(seq) - 1)]

    @jit
    def sample(self, ps, n):
        '''
        Use for numba compatibility - does not support choice or sample

        Returns:

        '''
        idx = range(0, len(ps))
        return [ps[x] for x in shuffle(idx)[0:n]]

    @jit
    def CreateRandomTeam(self):
        team = {
            'qb': self.sample(self.qbs, 1),
            'rb': self.sample(self.rbs, 2),
            'wr': self.sample(self.wrs, 3),
            'te': self.sample(self.tes, 1),
            'flex': self.sample(self.flexs, 1),
            'dst': self.sample(self.dsts, 1)
        }

        while True:
            flexer = team['flex'][0]
            if flexer in team['rb'] or flexer in team['wr'] or flexer in team['te']:
                team['flex'] = self.sample(self.flexs, 1)
            else:
                break

        return team

    @jit
    def GetTeamPointTotal(self, team):
        total_points = 0
        for pos, players in team.items():
            for player in players:
                total_points += player.points
        return total_points

    @jit
    def GetTeamSalary(self, team):
        total_salary = 0
        for pos, players in team.items():
            for player in players:
                total_salary += player.salary
        return total_salary

    @jit
    def printTeam(self, team):
        print team['qb'][0]
        print team['rb'][0]
        print team['rb'][1]
        print team['wr'][0]
        print team['wr'][1]
        print team['wr'][2]
        print team['te'][0]
        print team['flex'][0]
        print team['dst'][0]
        print '${}, {} points'.format(self.GetTeamSalary(team), self.GetTeamPointTotal(team))

    @jit
    def load_players(self, players, projection_formula=None, team_exclude=[], player_exclude=[], randomize_projections=True):
        '''
        Takes list of player dicts, returns list of Player objects
        :param players(list): of player dict
        :return: all_players(list): of Player
        '''
        all_players = []

        for p in players:
            oppos = str(p.get('Opposing_TeamFB', '').replace('@', ''))
            pos = str(p.get('Position'))
            if pos == 'D':
                pos = str('DST')
            team = str(p.get('Team'))
            player_name = str(p.get('Player_Name'))

            mean_projection = p.get('AvgPts', 0)
            ceiling = p.get('Ceiling', 0)
            floor = p.get('Floor', 0)

            if randomize_projections:
                projections = [mean_projection + round(mean_projection * uniform(-.05,.05), 2)]
                ceilings = [ceiling + round(ceiling * uniform(-.05,.05), 3)]
                floors = [floor + round(floor * uniform(-.05,.05), 3)]
            else:
                projections = [mean_projection]
                ceilings = [ceiling]
                floors = [floor]

            if projection_formula == 'cash':
                proj = (self.choice(projections) * .5) + (self.choice(ceilings) * .15) + (self.choice(floors) * .35)
            elif projection_formula == 'tournament':
                proj = (self.choice(projections) * .3) + (self.choice(ceilings) * .6) + (self.choice(floors) * .1)
            elif projection_formula == 'tourncash':
                proj = (self.choice(projections) * .4) + (self.choice(ceilings) * .3) + (self.choice(floors) * .3)
            elif ',' in projection_formula:
                avg, ceiling, floor = projection_formula.split(',')
                proj = (self.choice(projections) * avg) + (self.choice(ceilings) * ceiling) + (self.choice(floors) * floor)
            else:
                proj = self.choice(projections)

            if team in team_exclude:
                continue
            elif player_name in player_exclude:
                continue
            else:
                all_players.append(Player(projection=proj, position=pos, name=player_name, salary=p.get('Salary'), team=team, oppos=oppos))

        return all_players

    @jit
    def fitness(self, team):
        points = self.GetTeamPointTotal(team)
        salary = self.GetTeamSalary(team)
        values = team.values()
        if salary > 50000:
            return 0
        return points

    @jit
    def grade(self, pop):
        'Find average fitness for a population.'
        summed = reduce(add, (self.fitness(team) for team in pop))
        return summed / (len(pop) * 1.0)

    @jit
    def listToTeam(self, players):
        return {
            'qb': [players[0]],
            'rb': players[1:3],
            'wr': players[3:6],
            'te': [players[6]],
            'flex': [players[7]],
            'dst': [players[8]]
        }

    @jit
    def breed(self, mother, father):
        positions = ['qb', 'rb', 'wr', 'te', 'flex', 'dst']

        mother_lists = [mother['qb'] + mother['rb'] + mother['wr'] + mother['te'] + mother['flex'] + mother['dst']]
        mother_list = [item for sublist in mother_lists for item in sublist]
        father_lists = [father['qb'] + father['rb'] + father['wr'] + father['te'] + father['flex'] + father['dst']]
        father_list = [item for sublist in father_lists for item in sublist]

        index = self.choice([1, 3, 6, 7, 8])
        child1 = self.listToTeam(mother_list[0:index] + father_list[index:])
        child2 = self.listToTeam(father_list[0:index] + mother_list[index:])

        while True:
            flexer = child1['flex'][0]
            if flexer in child1['rb'] or flexer in child1['wr'] or flexer in child1['te']:
                child1['flex'] = self.sample(self.flexs, 1)
            else:
                break

        while True:
            flexer = child2['flex'][0]
            if flexer in child2['rb'] or flexer in child2['wr'] or flexer in child2['te']:
                child2['flex'] = self.sample(self.flexs, 1)
            else:
                break

        return [child1, child2]

    @jit
    def mutate(self, team):

        random_pos = self.choice(self.positions)
        if random_pos == 'qb':
            team['qb'][0] = self.choice(self.qbs)
        if random_pos == 'rb':
            team['rb'] = self.sample(self.rbs, 2)
        if random_pos == 'wr':
            team['wr'] = self.sample(self.wrs, 3)
        if random_pos == 'te':
            team['te'][0] = self.choice(self.tes)
        if random_pos == 'flex':
            team['flex'][0] = self.choice(self.flexs)
        if random_pos == 'dst':
            team['dst'][0] = self.choice(self.dsts)

        while True:
            flexer = team['flex'][0]
            if flexer in team['rb'] or flexer in team['wr'] or flexer in team['te']:
                team['flex'] = self.sample(self.flexs, 1)
            else:
                break
        return team

    @jit
    def evolve(self, pop, retain=0.25, random_select=0.10, mutate_chance=0.010):
        graded = [ (self.fitness(team), team) for team in pop]
        graded = [ x[1] for x in sorted(graded, reverse=True)]
        retain_length = int(len(graded)*retain)
        parents = graded[:retain_length]

        # randomly add other individuals to promote genetic diversity
        for individual in graded[retain_length:]:
            if random_select > random():
                parents.append(individual)

        # mutate some individuals
        for individual in parents:
            if mutate_chance > random():
                individual = self.mutate(individual)

        # crossover parents to create children
        parents_length = len(parents)
        desired_length = len(pop) - parents_length
        children = []
        while len(children) < desired_length:
            male = randint(0, parents_length-1)
            female = randint(0, parents_length-1)
            if male != female:
                male = parents[male]
                female = parents[female]
                babies = self.breed(male,female)
                for baby in babies:
                    children.append(baby)
        parents.extend(children)
        return parents

    @jit
    def run_solver(self, players, pop_size=10000, salary_cap=50000, points_floor=100):
        '''
        Produces lineups from genetic algorithm

        Args:
            players:
            pop_size:

        Returns:

        '''
        best_teams = []
        history = []
        p = self.CreatePopulation(pop_size)
        fitness_history = [self.grade(p)]
        for i in xrange(60):
            p = self.evolve(p)
            fitness_history.append(self.grade(p))
            valid_teams = [team for team in p if self.GetTeamSalary(team) <= salary_cap and self.GetTeamPointTotal(team) >= points_floor]
            valid_teams = sorted(valid_teams, key=self.GetTeamPointTotal, reverse=True)
            if len(valid_teams) > 0:
                best_teams.append(valid_teams[0])
        for datum in fitness_history:
            history.append(datum)

        return sorted(best_teams, key=self.GetTeamPointTotal, reverse=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import cPickle as pickle
    import os

    #from nfl.agents.fantasylabs import FantasyLabsNFLAgent
    from nfl.optimizers.genalg import GenAlg

    fn = '/home/sansbacon/players.pkl'
    ga = GenAlg()

    if os.path.exists(fn):
        with open(fn, 'rb') as infile:
            players = pickle.load(infile)

        names = {}
        for p in players:
            n = p.get('Player_Name')
            if names.get(n):
                continue
            else:
                names[n] = p
        ga.players = ga.load_players(players=names.values(), projection_formula='cash')

    else:
        '''
        a = FantasyLabsNFLAgent()
        d = '12_14_2016'
        players = a.model(d, 'levitan', 'dk')

        names = {}
        for p in players:
            n = p.get('Player_Name')
            if names.get(n):
                continue
            else:
                names[n] = p

        ga.players = ga.load_players(players=names.values(), projection_formula='cash')
        with open(fn, 'wb') as outfile:
            pickle.dump(ga.players, outfile)
        '''
        raise SystemExit


    # problem is not getting different lineups
    teams = ga.run_solver(ga.players, pop_size=10000)
    best = [teams.pop(0)]
    counter = 0
    max = 20
    for t in teams:
        if ga.GetTeamPointTotal(t) < ga.GetTeamPointTotal(best[-1]):
            if counter <= max:
                print ga.GetTeamPointTotal(best[-1])
                best.append(t)
                print 'added team, counter is {}'.format(counter)
                counter += 1
                print 'counter incremented to {}'.format(counter)
            else:
                break
