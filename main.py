"""

Driver program for scraping data and loading to database.

Can use this to rerun specific steps of the data load process

"""

import argparse
import logging
from data_collection.scrape import collect_recipe_data
from data_collection.load_data import load_files_to_db
from datetime import datetime

def init_logger():
    current_ts = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    logfile = f'logs/{current_ts}.txt'

    logging.basicConfig(
        filename=logfile,
        filemode='a',
        format='[%(asctime)s %(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    return logging.getLogger('cookit-scraper')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', 
        '--skip_collect', 
        action='store_true', 
        required=False, 
        help='specify this flag to skip the data collection step',
    )

    parser.add_argument(
        '-l', 
        '--skip_load', 
        action='store_true', 
        required=False, 
        help='specify this flag to skip the database load step',
    )

    return parser.parse_args()

def main():
    logger = init_logger()
    args = parse_arguments()
    
    skip_collect = args.skip_collect
    skip_load = args.skip_load

    if not skip_collect:
        logger.info('starting web scraping')
        collect_recipe_data()
        logger.info('finished collecting recipe data')
    if not skip_load:
        logger.info('starting database load')
        load_files_to_db()
        logger.info('finished loading files to database')

if __name__ == '__main__':
    main()
