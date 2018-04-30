import pymysql
import dbconfig


class DBHelper:

    def __init__(self):
        self.connection = None

    def connect(self, database="crimemap"):
        if not self.connection:
            self.connection = pymysql.connect(host='localhost',
                                              user=dbconfig.db_user,
                                              passwd=dbconfig.db_password,
                                              db=database)
        return self.connection

    def get_all_inputs(self):
        connection = self.connect()
        try:
            query = "SELECT description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            connection.close()

    def add_input(self, data):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (description) VALUES (%s);"
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                connection.commit()
        finally:
            connection.close()

    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()
