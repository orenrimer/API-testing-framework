import os

PATH_CONFIG = dict(
    ROOT=os.path.dirname(__file__),
    TEST=os.path.join(os.path.dirname(__file__), "tests"),
    TEST_DATA=os.path.join(os.path.dirname(__file__), "tests", "resources", "test_data")
)

HOST_CONFIG = dict(
    local="http://localhost/wpdemostore/wp-json/wc/v3/",
    test='',
    prod=''
)

DB_CONFIG = dict(
    local={
        'host': 'localhost',
        'database': 'wpdemostore',
        'table_prefix': 'wp_',
        'port': 3306,
    }
)
