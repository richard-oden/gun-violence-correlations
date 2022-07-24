import logging
import os
from logging.handlers import TimedRotatingFileHandler

def configure_logging():
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