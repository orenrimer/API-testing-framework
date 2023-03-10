import os


class CredentialUtils:
    @staticmethod
    def get_wc_api_credentials():
        wc_key = os.getenv('WC_KEY')
        wc_secret = os.getenv('WC_SECRET')

        if not wc_key or not wc_secret:
            raise Exception("API key or secret not in env")
        else:
            return {'key': wc_key, 'secret': wc_secret}

    @staticmethod
    def get_db_credentials():
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')

        if not db_user or db_password is None:
            raise Exception("DB credentials not in env")
        else:
            return {'user': db_user, 'password': db_password}
