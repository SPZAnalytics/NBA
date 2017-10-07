import collections
import logging


class FantasyLabsNBAParser(object):
    '''
    FantasyLabsNBAParser

    Usage:
        p = FantasyLabsNBAParser()
        games = p.games(games_json)
        model = p.model(model_json)
    '''

    def __init__(self):
        logging.getLogger(__name__).addHandler(logging.NullHandler())
                        
    def _flatten(self, d):
        '''
        Flattens nested dict into single dict

        Args:
            d: original dict

        Returns:
            dict
        '''
        items = []
        for k, v in d.items():
            if isinstance(v, collections.MutableMapping):
                items.extend(self._flatten(v).items())
            else:
                items.append((k, v))
        return dict(items)

    def dk_salaries(self, content, game_date):
        '''
        Gets list of salaries for one day
        Args:
            content (str):
            day(str): in mm_dd_YYYY format
        Returns:
            players (list): of player dict
        '''
        return self.model(content, site='dk', game_date=game_date)

    def model(self, content, site='dk', game_date=None):
        '''
        Parses dict associated with model (player stats / projections)
        The model has 3 dicts for each player: DraftKings, FanDuel, Yahoo
        SourceIds: 4 is DK, 11 is Yahoo, 3 is FD
        Arguments:
            content(dict):
            site(str):
            gamedate(str):
        Returns:
            players: list of parsed models
        Usage:
            model = p.model(content, site='dk', gamedate='1_14_2017')
        '''
        players = []
        for md in content.get('PlayerModels'):
            player = {'site': site}
            for k,v in list(md.items()):
                if k == 'Properties':
                    for k2,v2 in list(v.items()):
                        player[k2] = v2
                else:
                    player[k] = v
            if player.get('SourceId', None) == 4:
                players.append(player)
        return players

    def ownership(self, content, game_date=None):
        '''
        Parses ownership json
        Args:
            content: parsed json
            game_date: datestr

        Returns:
            list of players with ownership percentages
        '''
        #omit = ['ErrorList', 'ActualPoints', 'ActualPoints_pct', 'ActualPoints_rnk', 'Average', 'SortValue',
        #        'Player_Name_pct', 'Player_Name_rnk', 'Team_pct', 'Team_rnk']
        #return [{k: v for k, v in self._flatten(pl).items() if k not in omit} for pl in content]
        vals = [self._flatten(pl) for pl in content]
        if game_date:
            for idx, _ in enumerate(vals):
                vals[idx]['game_date'] = game_date
        return vals

if __name__ == "__main__":
    pass
