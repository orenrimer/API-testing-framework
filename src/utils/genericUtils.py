import json
import random
import string


def generate_random_string(prefix=None, suffix=None, length=10):
    random_string = "".join(random.choices(string.ascii_lowercase, k=length))
    if prefix:
        random_string = str(prefix) + "_" + random_string
    elif suffix:
        random_string += str(suffix)
    return random_string


def generate_random_email(domain=None, prefix=None, length=10):
    if not domain:
        domain = 'gmail.com'
    if not prefix:
        prefix = "testuser"

    random_string = "".join(random.choices(string.ascii_lowercase, k=length))
    random_email = prefix + '_' + random_string + '@' + domain
    return random_email


def generate_random_password(length=10):
    password_string = "".join(random.choices(string.ascii_letters, k=length))
    return password_string


def read_data_from_json(file_path):
    data = {}

    try:
        with open(file_path, 'r') as f:
            data.update(json.load(f))
    except IOError:
        raise IOError(f"File '{file_path}' not found.")

    return data
