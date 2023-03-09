import pymysql.cursors
from config import DB_CONFIG
from src.utils.credentialUtils import CredentialUtils


class DbUtils:
    def __init__(self):
        self.credentials = CredentialUtils.get_db_credentials()
        self.host = DB_CONFIG['local']['host']
        self.port = DB_CONFIG['local']['port']
        self.db = DB_CONFIG['local']['database']

    def connect(self):
        connection = pymysql.connect(host=self.host,
                                     user=self.credentials['user'],
                                     password=self.credentials['password'],
                                     db=self.db,
                                     port=self.port)
        return connection

    def select(self, sql):
        connection = self.connect()
        try:
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            response = cursor.fetchall()
            cursor.close()
        except Exception as e:
            raise Exception(f"Failed running query '{sql}'\nError: {str(e)}")
        finally:
            connection.close()

        return response
