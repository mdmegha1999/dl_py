"""
For managing logs at one place.

Functions:

    init_logger(string) -> object
    get_logger(string) -> object

"""
import os
import logging

os.makedirs("./log", exist_ok=True)


def init_logger(name: str) -> object:
    """
    Returns the logger object.

            Parameters:
                    name (str): string - file name

            Returns:
                    logger (object): return the logger object
    """
    log = "./log/"
    logger = logging.getLogger(name)
    logger_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_handler = logging.FileHandler(f"{log+str(name)}.log")
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(logging.Formatter(logger_format))
    logger.addHandler(log_handler)
    stream_h = logging.StreamHandler()
    stream_h.setLevel(logging.DEBUG)
    stream_h.setFormatter(logging.Formatter(logger_format))
    logger.addHandler(stream_h)
    logger.setLevel(logging.DEBUG)
    return logger


def get_logger(name: str) -> object:
    """
    Returns the logger object.

            Parameters:
                    name (str): string - file name

            Returns:
                    logger (object): return the logger object
    """
    return logging.getLogger(name)
