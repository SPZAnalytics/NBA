from collections import defaultdict
import logging

from nba.agents.agent import NBAAgent


class RotoguruNBAAgent(NBAAgent):
    '''
    Performs script-like tasks using rotoguru scraper and parser
    Intended to replace standalone scripts so can use common API and tools

    Examples:
        a = RotoguruNBAAgent()

    '''

    def __init__(self, **kwargs):
        logging.getLogger(__name__).addHandler(logging.NullHandler())

        # see http://stackoverflow.com/questions/8134444
        NBAAgent.__init__(self, **kwargs)

    def rg_salaries(self, salary_pages, players_fname, site):
        '''
        Parses list of rotoguru pages into list of salary dictionaries

        Arguments:
            salary_pages (dict): keyed by gamedate, value is HTML
            players_fname (str): is full path of csv file with players
            site (str): name of site - dk, fd, yh . . .

        Returns:
            salaries (list): list of salary dictionaries
            players (dict): keys are player name, values are player id
            unmatched (defaultdict): keys are playername, values is counter

        Usage:
            salaries = NBAComAgent.rotoguru_dfs_salaries(salary_pages, '~/players.csv', 'dk')
            NBAComAgent.nbadb.insert_dicts(salaries, 'salaries')

        '''

        salaries = []
        players = {}
        unmatched = defaultdict(int)

        players = self._players_from_csv(players_fname)

        for key in sorted(salary_pages.keys()):
            daypage = salary_pages.get(key)

            for sal in p.salaries(daypage, site):

                # players is key of nbacom_name and value of nbacom_id
                # need to match up rotoguru names with these
                pid = players.get(sal.get('site_player_name'), None)

                # if no match, try conversion dictionary
                if not pid:
                    nba_name = self.nbap.rg_to_nbadotcom(sal.get('site_player_name', None))
                    pid = players.get(nba_name, None)

                # if still no match, warn and don't add to database
                if not pid:
                    logging.warning('no player_id for {0}'.format(sal.get('site_player_name')))
                    unmatched[sal.get('site_player_name')] += 1
                    continue

                else:
                    sal['nbacom_player_id'] = pid

                # if no salary, warn and don't add to database
                if not sal.get('salary', None):
                    logging.warning('no salary for {0}'.format(sal.get('site_player_name')))
                    continue

                salaries.append(sal)

        return salaries, players, unmatched

if __name__ == '__main__':
    pass
