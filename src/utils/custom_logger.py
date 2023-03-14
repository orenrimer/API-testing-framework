import logging
from os import path
import time
from settings import DIRS


def set_logger_config(level=logging.INFO):
    file_name = "log_" + str(round(time.time() * 1000)) + ".txt"
    logger_path = path.join(DIRS["RESOURCES"], "logs", file_name)

    file_handler = logging.FileHandler(logger_path, mode="w")
    file_handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s :: %(filename)s:%(lineno)d  :: %(levelname)s :: %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    logging.root.setLevel(level)
    logging.root.addHandler(file_handler)
