import logging
import os
import time
from datetime import datetime

logger = None


def configure_logging() -> None:
    '''
    Configures logging for the application. Logs are divided into separate files by day and saved in /static/logs.
    '''
    logs_directory = os.path.join('src', 'static', 'logs')
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    global logger
    logger = logging.getLogger('application')
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(
        filename=os.path.join(logs_directory, f'{datetime.now().strftime("%Y-%m-%d")}_log.txt'))
    handler.formatter = logging.Formatter(
        fmt='%(asctime)s -- [%(levelname)s]: %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p')
        
    logger.addHandler(handler)


def log_info(message: str) -> None:
    '''
    Logs a message with severity INFO.

    Parameters
    ---
    `message` : `str` representing the message to be logged
    '''
    logger.info(message)

def log_error(message: str) -> None:
    '''
    Logs a message with severity ERROR.

    Parameters
    ---
    `message` : `str` representing the message to be logged
    '''
    logger.error(message)

def start_timed_log(message: str) -> float:
    '''
    Logs a message with severity INFO and returns a float representing the current time.

    Parameters
    ---
    `message` : `str` representing the message to be logged

    Returns
    ---
    `float` representing the current time in seconds since epoch
    '''
    logger.info(message)
    return time.time()

def stop_timed_log(message: str, start_time: float) -> None:
    '''
    Logs a message with severity INFO that contains the number of seconds that have elpased since `start_time`.

    Parameters
    ---
    `message` : `str` representing the message to be logged
    `start_time` : `float` representing the start time in seconds since epoch
    '''

    logger.info(f'{message} Time elapsed: {round((time.time() - start_time), 2)}s')