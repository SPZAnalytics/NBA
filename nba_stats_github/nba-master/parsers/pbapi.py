import json
import logging

class ProBasketballAPIParser(object):

    def __init__(self):
        logging.getLogger(__name__).addHandler(logging.NullHandler())

    def players(self, content):

        player_ids = {p.get('player_id'): '{0} {1}'.format(p.get('first_name'), p.get('last_name')) for p in content}

        '''
        stats.player_xref
          nbacom_player_id integer NOT NULL,
          site character varying(30) NOT NULL,
          site_player_name character varying(50) NOT NULL,
          site_player_id integer,
        '''
