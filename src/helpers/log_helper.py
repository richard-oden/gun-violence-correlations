import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

def configure_logging() -> None:
    '''
    Configures logging for the application. Logs are divided into separate files by day and saved in /static/logs.
    '''
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
    '''
    Logs a message with severity INFO.

    Parameters
    ---
    `message` : `str` representing the message to be logged.
    '''
    logging.info(message)

def log_error(message: str) -> None:
    '''
    Logs a message with severity ERROR.

    Parameters
    ---
    `message` : `str` representing the message to be logged.
    '''
    logging.error(message)

def start_timed_log(message: str) -> float:
    '''
    Logs a message with severity INFO and returns.

    Parameters
    ---
    `message` : `str` representing the message to be logged.
    '''
    logging.info(message)
    return time.time()

def stop_timed_log(message: str, start_time: float) -> float:
    logging.info(message)
    return round((time.time() - start_time), 2)