import datetime as dt
import logging
import os
import subprocess

from builtins import range

import psycopg2
import psycopg2.extras


class NBAPostgres(object):

    def __init__(self, user, password, database, chunk_size=5000):
        '''
        Arguments:
            user (str): postgres username
            database (str): postgres database name

        '''
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        self.conn = psycopg2.connect(dbname=database, user=user, password=password)
        self.chunk_size = chunk_size

    def _chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]


    def _insert_dict(self, dict_to_insert, table_name):
        '''
        Generic routine to insert dictionary into table. Use as a backup when insert_dicts fails

        Arguments:
            dict_to_insert: list of dicts
            table_name: string
        '''
        cursor = self.conn.cursor()
        placeholders = ', '.join(['%s'] * len(dict_to_insert))
        columns = ', '.join(dict_to_insert.keys())
        sql = 'INSERT INTO %s ( %s ) VALUES ( %s ) ON CONFLICT DO NOTHING;' % (table_name, columns, placeholders)
        try:
            cursor.execute(sql, dict_to_insert.values())
            logging.info(cursor.query)
            self.conn.commit()
        except Exception as e:
            logging.exception('insert_dicts failed: {0}'.format(e))
            self.conn.rollback()
        finally:
            cursor.close()


    def execute(self, sql):
        '''
        Generic routine to execute statement
        Will rollback with any errors

        Arguments:
            sql(str): statement

        Returns:
            None
        '''
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            logging.exception('update failed: {0}'.format(e))
            self.conn.rollback()
        finally:
            cursor.close()


    def insert_dicts(self, dicts_to_insert, table_name):
        '''
        Generic routine to insert dictionary into mysql table
        Will rollback with any errors

        Arguments:
            dicts_to_insert(list): list of dictionaries to insert, keys match columns
            table_name(str): name of database table

        Returns:
            None
        '''
        if not dicts_to_insert:
            raise ValueError('nothing to insert')

        # https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query/30985541#30985541
        # postgresql will convert list of tuples into postgres records
        cur = self.conn.cursor()

        for chunk in self._chunks(dicts_to_insert, self.chunk_size):
            fields = tuple(sorted(chunk[0].keys()))
            records = []
            for d in dicts_to_insert:
                t = tuple([d[f] for f in fields])
                records.append(t)
            records_list_template = ','.join(['%s'] * len(records))
            insert_query = 'insert into {0} ({1}) values {2} ON CONFLICT DO NOTHING'.format(table_name, ','.join(fields), records_list_template)

            try:
                cur.execute(cur.mogrify(insert_query, records))
                self.conn.commit()
            except Exception as e:
                logging.error('insert statement is {0}'.format(insert_query))
                logging.exception('insert_dicts failed: {0}'.format(e.diag.message_primary))
                self.conn.rollback()

        cur.close()


    def postgres_backup_db(self, dbname, dirname=None):
        '''
        Compressed backup of database

        Args:
            dbname (str): the name of the database
            dirname (str): the name of the backup dirnameectory, default is home

        Returns:
            None           
        '''

        if not dirname or not os.path.exists(dirname):
            dirname = os.path.expanduser('~')

        bdate = dt.datetime.now().strftime('%Y%m%d%H%M')
        bfile = os.path.join(dirname, '{0}_{1}.sql'.format(dbname ,bdate))

        cmd = ['pg_dump', "-Upostgres", "--compress=9", "--file=" + bfile, dbname]
        p = subprocess.Popen(cmd)
        retcode = p.wait()

        if retcode > 0:
            print('Error:', dbname, 'backup error')


    def postgres_backup_table(self, dbname, tablename, dirname=None, username='postgres'):
        '''
        Compressed backup of mysql database table
        Based on https://mcdee.com.au/python-mysql-backup-script/

        Args:
            dbname (str): the name of the mysql database
            tablename (str): the name of the mysql database table
            dirname (str): the name of the backup dirnameectory, default is home

        Returns:
            None           
        '''

        if not dirname or not os.path.exists(dirname):
            dirname = os.path.expanduser('~')

        bdate = dt.datetime.now().strftime('%Y%m%d%H%M')
        bfile = os.path.join(dirname, '{0}_{1}_{2}.sql.gz'.format(dbname, tablename, bdate))

        cmd = ['pg_dump', "--table=" + tablename, "--username=" + username, "--compress=9", "--file=" + bfile, dbname]
        p = subprocess.Popen(cmd)
        retcode = p.wait()

        if retcode > 0:
            print('Error:', dbname, 'backup error')


    def select_dict(self, sql):
        '''
        Generic routine to get list of dictionaries from table

        Arguments:
            sql (str): the select statement you want to execute

        Returns:
            results (list): list of dictionaries representing rows in table
        '''

        cursor = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        try:
            cursor.execute(sql)
            return cursor.fetchall()

        except Exception as e:
            logging.exception(e.message)
            self.conn.rollback()
            return None

        finally:
            cursor.close()


    def select_list(self, sql):
        '''
        Generic routine to get list of values from one column of table

        Arguments:
            sql (str): the select statement you want to execute

        Returns:
            results (list): list of rows in column
        '''

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            return [v[0] for v in cursor.fetchall()]

        except Exception as e:
            logging.error('sql statement failed: {0}'.format(sql))
            self.conn.rollback()
            return None

        finally:
            cursor.close()


    def select_scalar(self, sql):
        '''
        Generic routine to get a single value from a table

        Arguments:
            sql (str): the select statement you want to execute

        Returns:
            result: type depends on the query
        '''

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            return cursor.fetchone()[0]

        except Exception as e:
            logging.error('sql statement failed: {0}'.format(sql))
            self.conn.rollback()
            return None

        finally:
            cursor.close()


    def update(self, sql):
        '''
        Generic routine to update table
        Will rollback with any errors

        Arguments:
            sql(str): UPDATE statement

        Returns:
            None
        '''

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            self.conn.commit()

        except Exception as e:
            logging.exception('update failed: {0}'.format(e.message))
            self.conn.rollback()

        finally:
            cursor.close()


if __name__ == '__main__':
    pass