

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

    def post_news(self, x):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = "INSERT INTO `news` VALUES(0, '{}', CURRENT_DATE)".format(x)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return "News Posted"

    def delete_news(self, x):
        cursorx = self.connection.cursor(dictionary=True, buffered=True)
        sqlx = "SELECT * FROM `news` WHERE id = '{}'".format(x)
        cursorx.execute(sqlx)
        if cursorx.rowcount == 0:
            self.connection.commit()
            cursorx.close()
            return "No news with id"
        else:

            cursor = self.connection.cursor(dictionary=True, buffered=True)
            sql = "DELETE FROM `news` WHERE id = '{}'".format(x)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return "News Deleted"

    def update_news(self, x, y):
        cursorx = self.connection.cursor(dictionary=True, buffered=True)
        sqlx = "SELECT * FROM `news` WHERE id = '{}'".format(x)
        cursorx.execute(sqlx)
        if cursorx.rowcount == 0:
            self.connection.commit()
            cursorx.close   
            return "No news with id"
        else:
            cursor = self.connection.cursor(dictionary=True, buffered=True)
            sql = "UPDATE `news` SET newsdesc = '{}', date = CURRENT_DATE WHERE id = 4;".format(y)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return "News updated"
        

    def get_all_news(self):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql ="SELECT * FROM `news` WHERE date >= DATE_SUB(curdate(), INTERVAL 1 MONTH)"
        result = []
        cursor.execute(sql)
        for i in cursor.fetchall():
            result.append({
                'id': i['id'],
                'desc': i['newsdesc'],
                'date': i['date']
            })
        cursor.close()
        return result

    def get_news(self, x):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = "SELECT * FROM `news` WHERE `id` = '{}'".format(x)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result



class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=32,
                pool_reset_session=True,
                host='localhost',
                database='personalportofolio_news',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())