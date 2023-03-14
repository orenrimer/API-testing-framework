import random
from src.utils.dbUtils import DbUtils


class CustomerDB:
    def __init__(self, host, port, db_name):
        self.db = DbUtils(host, port, db_name)
        self.TABLE_NAME = f"{db_name}.wp_users"

    def select_customer_by_email(self, email):
        """
        select a customer from the db using email
        """
        return self.db.select([self.TABLE_NAME], where=f"user_email = '{email}'")

    def select_customer_by_id(self, customer_id):
        """
        select a customer from the db using customer id
        """
        response = self.db.select([self.TABLE_NAME], where=f"ID = {customer_id}")
        return response

    def select_random_customer(self, order_by=None, qty=1):
        """
        select a random customer from the db (excluding root user)
        """
        response = self.db.select(
            [self.TABLE_NAME], where="ID <> 1", order_by=order_by, limit=qty
        )
        return random.sample(response, k=int(qty))

    def select_all_customer(self):
        """
        select all customers from the database (excluding root user)
        """
        return self.db.select([self.TABLE_NAME], where="ID <> 1")
