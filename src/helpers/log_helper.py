import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

def configure_logging() -> None:
    logging.basicConfig(
        format='%(asctime)s -- [%(levelname)s]: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO)
    handler = TimedRotatingFileHandler(
        filename=os.path.join('static', 'logs', 'log.txt'), 
        when='midnight', 
        interval=1)
    handler.suffix = "%Y-%m-%d"

    logging.getLogger().addHandler(handler)


def log_info(message: str) -> None:
    logging.info(message)

def log_error(message: str) -> None:
    logging.error(message)

def start_timed_log(message: str) -> float:
    logging.info(message)
    return time.time()

def stop_timed_log(message: str, start_time: float) -> None:
    logging.info(message)
    return round((time.time() - start_time), 2)