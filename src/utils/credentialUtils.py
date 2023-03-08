from secret import API_CRED, DB_CRED


class CredentialUtils:
    @staticmethod
    def get_wc_api_credentials():
        if 'WC_KEY' not in API_CRED or 'WC_SECRET' not in API_CRED:
            raise Exception("API key or secret not found")
        else:
            return {'key': API_CRED['WC_KEY'], 'secret': API_CRED['WC_SECRET']}

    @staticmethod
    def get_db_credentials():
        if 'DB_USER' not in DB_CRED or 'DB_PASSWORD' not in DB_CRED:
            raise Exception("DB credentials not not found")
        else:
            return {'user': DB_CRED['DB_USER'], 'password': DB_CRED['DB_PASSWORD']}
