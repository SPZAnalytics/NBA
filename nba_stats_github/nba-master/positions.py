import MySQLdb
import pandas as pd

class NBAPositions(object):

    def fix_positions():
        '''
        f = pd.read_csv('/home/sansbacon/FIXED_current_players.csv')
        f.ix[f.nbacom_position =='Center', 'primary_position'] = 'C'
        f.ix[f.nbacom_position =='Center-Forward', 'position_group'] = 'Big'
        f.ix[f.nbacom_position =='Center-Forward', 'primary_position'] = 'C'
        f.ix[f.nbacom_position =='Forward-Center', 'position_group'] = 'Big'
        f.ix[f.nbacom_position =='Forward-Center', 'primary_position'] = 'PF'
        f.ix[f.nbacom_position =='Guard-Forward', 'position_group'] = 'Wing'
        f.ix[f.nbacom_position =='Guard-Forward', 'primary_position'] = 'SG'
        f.ix[f.nbacom_position =='Forward-Guard', 'position_group'] = 'Wing'
        f.ix[f.nbacom_position =='Forward-Guard', 'primary_position'] = 'SF'
        '''

        f = pd.read_csv('/home/sansbacon/stilltofix.csv')
        players = f.to_dict('records')

        conn = MySQLdb.connect(host='localhost', user=PWD, passwd=PWD, db='nba_dot_com')
        cursor = conn.cursor()

        try:
            for player in players:
                sql = '''UPDATE players SET primary_position = "{0}", position_group = "{1}" WHERE person_id = "{2}"'''
                cursor.execute(sql.format(player['primary_position'], player['position_group'], player['person_id']))

            conn.commit()

        except Exception as e:
            print(e.message)
            conn.rollback()

        finally:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    pass
