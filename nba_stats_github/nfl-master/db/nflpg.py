import datetime as dt
import logging
import os
import pprint
import subprocess

import psycopg2
import psycopg2.extras


class NFLPostgres(object):

    def __init__(self, user, password, database='nfl'):
        '''
        Arguments:
            user (str): postgres username
            database (str): postgres database name

        '''

        self.logger = logging.getLogger(__name__)
        self.user = user
        self.password = password
        self.database = database
        self.conn = psycopg2.connect('dbname={0} user={1} password={2}'.format(self.database, self.user, self.password))

    def _insert_dict(self, dict_to_insert, table_name):
        '''
        Generic routine to insert dictionary into mysql table
        TODO: not sure what purpose serving - not called by insert_dicts
        '''

        cursor = self.conn.cursor()
        placeholders = ', '.join(['%s'] * len(dict_to_insert))
        columns = ', '.join(dict_to_insert.keys())
        sql = 'INSERT INTO %s ( %s ) VALUES ( %s )' % (table_name, columns, placeholders)

        try:
            cursor.execute(sql, dict_to_insert.values())
            self.conn.commit()

        except Exception as e:
            self.logger.error('insert statement is {0}'.format(sql))
            self.logger.error(pprint.pformat(dict_to_insert))
            self.logger.exception('insert_dicts failed: {0}'.format(e.message))
            self.conn.rollback()

        finally:
            cursor.close()

    def batch_update(self, statements):
            '''
            Generic routine to update table with multiple statements
            Will rollback with any errors

            Arguments:
                statements(list): list of UPDATE statements

            Returns:
                None
            '''

            cursor = self.conn.cursor()

            try:
                for statement in statements:
                    cursor.execute(statement)
                self.conn.commit()

            except Exception as e:
                self.logger.exception('update failed: {0}'.format(e.message))
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

        if dicts_to_insert:
            cursor = self.conn.cursor()

            try:
                for dict_to_insert in dicts_to_insert:
                    placeholders = ', '.join(['%s'] * len(dict_to_insert))
                    columns = ', '.join(dict_to_insert.keys())
                    sql = 'INSERT INTO %s ( %s ) VALUES ( %s ) ON CONFLICT DO NOTHING' % (table_name, columns, placeholders)
                    cursor.execute(sql, dict_to_insert.values())

                self.conn.commit()

            except Exception as e:
                #if sql:
                #    self.logger.error('insert statement is {0}'.format(sql))
                #    self.logger.error('values are {0}'.format(','.join([str(v) for v in dict_to_insert.values()])))
                self.logger.exception('insert_dicts failed: {0}'.format(e))
                #if dict_to_insert:
                #    self.logger.error(pprint.pformat(dict_to_insert))

                self.conn.rollback()

            finally:
                cursor.close()
                
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
            self.logger.exception(e.message)
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
            self.logger.error('sql statement failed: {0}'.format(sql))
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
            self.logger.error('sql statement failed: {0}'.format(sql))
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
            self.logger.exception('update failed: {0}'.format(e.message))
            self.conn.rollback()

        finally:
            cursor.close()

if __name__ == '__main__':
    pass
