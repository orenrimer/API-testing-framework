from os.path import join, dirname

DIRS = dict(
    ROOT=dirname(__file__),
    TEST=join(dirname(__file__), "tests"),
    RESOURCES=join(dirname(__file__), "tests", "resources"),
    TEST_DATA=join(dirname(__file__), "tests", "resources", "test_data")
)
