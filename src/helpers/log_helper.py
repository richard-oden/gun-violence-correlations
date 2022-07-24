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
        filename=os.path.join('src', 'static', 'logs', 'log.txt'), 
        when='midnight', 
        interval=1)
    handler.suffix = "%Y-%m-%d"

    logging.getLogger().addHandler(handler)


def log_info(message: str) -> None:
    '''
    Logs a message with severity INFO.

    Parameters
    ---
    `message` : `str` representing the message to be logged
    '''
    logging.info(message)

def log_error(message: str) -> None:
    '''
    Logs a message with severity ERROR.

    Parameters
    ---
    `message` : `str` representing the message to be logged
    '''
    logging.error(message)

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
    logging.info(message)
    return time.time()

def stop_timed_log(message: str, start_time: float) -> None:
    '''
    Logs a message with severity INFO that contains the number of seconds that have elpased since `start_time`.

    Parameters
    ---
    `message` : `str` representing the message to be logged
    `start_time` : `float` representing the start time in seconds since epoch
    '''

    logging.info(f'{message} Time elapsed: {round((time.time() - start_time), 2)}s')