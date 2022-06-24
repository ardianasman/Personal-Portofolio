

from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling


class DatabaseWrapper:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    def register(self,x,y):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = '''INSERT INTO `user` (`username`, `password`) VALUES ('{}', '{}');'''.format(x,y)
        cursor.execute(sql)
        self.connection.commit()
        return "Register Completed"
    
    def login(self,x,y):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = "SELECT * FROM `user` WHERE `username` = '{}'".format(x)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            cursor.close()
            return 0
        else:
            resultf = cursor.fetchone()
            if(resultf['password'] == str(y)):
                cursor.close()
                return 1
            else:
                return 0
    
    def logout(self):
        self.connection.close()



class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=32,
                pool_reset_session=True,
                host='localhost',
                database='personalportofolio_paper',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())