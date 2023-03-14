from sqlalchemy import create_engine, MetaData, Table, desc, text, join
from src.utils.credentialUtils import CredentialUtils
from sqlalchemy.sql import select


class DbUtils:
    def __init__(self, host, port, db):
        self.host = host
        self.port = port
        self.db = db
        self.credentials = CredentialUtils.get_db_credentials()

    def connect(self):
        url = f'mysql+pymysql://{self.credentials["user"]}:{self.credentials["password"]}@{self.host}/{self.db}'
        engine = create_engine(url)
        return engine

    def select(self, tables, where=None, order_by=None, limit=None):
        engine = self.connect()

        try:
            metadata = MetaData()
            metadata.reflect(engine, schema=self.db)

            table_objs = [
                Table(table_name, metadata, autoload_with=engine)
                for table_name in tables
            ]
            query = select(*table_objs)
            if where:
                query = query.where(text(where))
            if order_by:
                query = query.order_by(desc(order_by))
            if limit:
                query = query.limit(limit)

            with engine.connect() as connection:
                cursor_result = connection.execute(query)
                keys = cursor_result.keys()
                res = cursor_result.fetchall()
                return [dict(zip(keys, list(r))) for r in res]
        except Exception as e:
            raise Exception(f"Failed running query\nError: {str(e)}")
