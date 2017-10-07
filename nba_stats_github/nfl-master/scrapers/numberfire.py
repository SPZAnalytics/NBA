import logging

<<<<<<< HEAD
from ewt.scraper import EWTScraper
=======
from EWTScraper import EWTScraper
>>>>>>> ace1da00fd9afc9f38280055e9751ec1562994bb


class NumberfireNFLScraper(EWTScraper):

    '''
    Obtains content of NFL fantasy projections page of fantasyfootballnerd.com
    Content will be a dictionary of projections and rankings
    Rankings are not position specific, projections are position-specific
    So structure will be rankings: [list of players], projections: {position: [list of players]}

    Example:
        s = FFNerdNFLScraper(api_key=os.environ.get('FFNERD_API_KEY'))
        content = s.get_projections()
    '''

    def __init__(self, **kwargs):
        '''
        '''

        # see http://stackoverflow.com/questions/8134444/python-constructor-of-derived-class
        EWTScraper.__init__(self, **kwargs)

        ' logger nullhandler

    def get_projections(self):
        """
        """

        url = 'http://www.numberfire.com/nfl/fantasy/fantasy-football-projections'
        
        projections = {}

        return projections

if __name__ == "__main__":
    pass
