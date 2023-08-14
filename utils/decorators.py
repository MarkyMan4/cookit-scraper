import logging
from datetime import datetime


def time_function(func):
    def wrapper_function(*args, **kwargs):
        logger = logging.getLogger('cookit-scraper')
        start_time = datetime.now()
        func(*args,  **kwargs)
        end_time = datetime.now()
        time_diff = end_time - start_time
        
        logger.info(f'function {func.__name__} finished in {time_diff}')

    return wrapper_function
