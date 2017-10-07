import logging
import pprint

from ewt.scraper import EWTScraper


class FFNerdNFLScraper(EWTScraper):

    '''
    Obtains content of NFL fantasy projections page of fantasyfootballnerd.com
    Content will be a dictionary of projections and rankings
    Rankings are not position specific, projections are position-specific
    So structure will be rankings: [list of players], projections: {position: [list of players]}

    Example:
        s = FFNerdNFLScraper(api_key=os.environ.get('FFNERD_API_KEY'))
        content = s.get_projections()
    '''

    def __init__(self, api_key, positions=['QB', 'RB', 'WR', 'TE'], response_format='json', league_format='standard', **kwargs):
        '''
        Args:
            api_key (str): Must specify API key for successful requests
        '''

        # see http://stackoverflow.com/questions/8134444/python-constructor-of-derived-class
        EWTScraper.__init__(self, **kwargs)

        self.api_key = api_key
        self.positions = positions
        self.response_format = response_format
        self.league_format = league_format

    def _generate_urls(self, **kwargs):
        """

        :param positions (list):
        :param response_format (str): json or xml, default is json
        :param league_format: standard or ppr, default is ppr
        :return list(str): urls for rankings and projection resources
        """

        # use defaults from instantiation or can pass new values

        if 'positions' in 'kwargs':
            positions = kwargs['positions']
        else:
            positions = self.positions

        if 'response_format' in 'kwargs':
            response_format = kwargs['response_format']
        else:
            response_format = self.response_format

        if 'league_format' in 'kwargs':
            league_format = kwargs['league_format']
        else:
            league_format = self.league_format

        urls = {'rankings': [], 'projections': {}}

        # add the rankings url
        if league_format == 'ppr':
            urls['rankings'].append('http://www.fantasyfootballnerd.com/service/draft-rankings/{0}/{1}/{2}/'.format(response_format, self.api_key, '1'))
        else:
            urls['rankings'].append('http://www.fantasyfootballnerd.com/service/draft-rankings/{0}/{1}/{2}/'.format(response_format, self.api_key, '0'))

        # now do the positional urls
        valid_positions = ['QB', 'RB', 'WR', 'TE', 'DEF', 'K']

        # you can pass a list of positions, have to check if valid
        for position in positions:
            if position in valid_positions:
                urls['projections'][position] = 'http://www.fantasyfootballnerd.com/service/draft-projections/{0}/{1}/{2}/'.format(response_format, self.api_key, position)
            else:
                logging.warn('%s not valid' % position)

        logging.debug('urls: %s' % pprint.pformat(urls))
        return urls

    def season_projections(self):
        """
        Gets rankings and projections, can assemble together with parser
        :return projections(dictionary): keys are positions, values are lists of player dictionaries
        :return rankings(list): list of player dictionaries
        """

        rankings = []
        projections = {}

        # loop through urls and fetch them
        for url_type, url_values in self._generate_urls().items():

            # rankings value will be a list (typically 1 item)
            if url_type == 'rankings':
                for url_value in url_values:
                    rankings.append(self.get(url_value))

            # projections value will be a dictionary
            elif url_type =='projections':
                for position, url in url_values.items():
                    projections[position] = self.get(url)
            else:
                pass

        return projections, rankings

    def weekly_projections(self, week, positions = ['QB', 'RB', 'WR', 'TE', 'DEF']):
        proj_url = 'http://www.fantasyfootballnerd.com/service/weekly-projections/{format}/{api_key}/{pos}/{week}/'
        projections = {pos: self.get(proj_url.format(format='json', api_key=self.api_key, pos=pos, week=week)) for pos in positions}
        rank_url = 'http://www.fantasyfootballnerd.com/service/weekly-rankings/{format}/8x3g9y245w6a/{pos}/{week}/1'
        rankings = {pos: self.get(rank_url.format(format='json', api_key=self.api_key, pos=pos, week=week)) for pos in positions}
        return projections, rankings

if __name__ == "__main__":
    pass
