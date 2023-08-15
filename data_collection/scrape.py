"""

Handles scraping recipe data and storing it as intermediate JSON files

"""

import json
import logging
import requests
import time
import traceback
from bs4 import BeautifulSoup
from random import random
from recipe_scrapers import scrape_me
from utils.decorators import time_function


CATEGORY_PAGE_URL = 'https://www.allrecipes.com/recipes-a-z-6735880'
CATEGORY_LINK_CLASS = 'link-list__link'
RECIPE_LINK_CLASS = 'comp mntl-card-list-items mntl-document-card mntl-card card card--no-image'

logger = logging.getLogger('cookit-scraper')

def scrape_recipe(url: str) -> dict:
    scraper = scrape_me(url)

    # some of these fields aren't in every recipe, so we will leave them null and still create the file
    # instead of throwing an error
    # if a field is not included in this exception handling, they are mandatory and I want to throw an
    # error if they are missing
    try:
        total_time = scraper.total_time()
    except Exception:
        logger.warn(f'field "total_time" is missing from recipe {url}')
        total_time = None

    try:
        image = scraper.image()
    except Exception:
        logger.warn(f'field "image" is missing from recipe {url}')
        image = None

    try:
        yields = scraper.yields()
    except Exception:
        logger.warn(f'field "yields" is missing from recipe {url}')
        yields = None

    try:
        cuisine = scraper.cuisine()
    except Exception:
        logger.warn(f'field "cuisine" is missing from recipe {url}')
        cuisine = None

    try:
        prep_time = scraper.prep_time()
    except Exception:
        logger.warn(f'field "prep_time" is missing from recipe {url}')
        prep_time = None

    try:
        cook_time = scraper.cook_time()
    except Exception:
        logger.warn(f'field "cook_time" is missing from recipe {url}')
        cook_time = None
    
    recipe_data = {
        'title': scraper.title(),
        'total_time': total_time,
        'image': image,
        'ingredients': scraper.ingredients(),
        'instructions': scraper.instructions(),
        'instructions_list': scraper.instructions_list(),
        'yields': yields,
        'nutrients': scraper.nutrients(),
        'cuisine': cuisine,
        'category': scraper.category(),
        'prep_time': prep_time,
        'cook_time': cook_time,
    }

    return recipe_data

def save_recipe_data(recipe_data: dict):
    file_name = recipe_data['title'].lower().replace(' ', '_') + '.json'
    
    with open(f'data/{file_name}', 'w') as f:
        json.dump(recipe_data, f)

def make_soup(url: str) -> BeautifulSoup:
    res = requests.get(url)
    return BeautifulSoup(res.text)

@time_function
def collect_recipe_data():
    soup = make_soup(CATEGORY_PAGE_URL)
    category_links = soup.find_all('a', class_=CATEGORY_LINK_CLASS)

    recipes_collected = 0

    # initial page is categories, each category has links to actual recipes
    # scrape each category link for links to recipes
    for cl in category_links:
        try:
            category_soup = make_soup(cl['href'])
            recipe_links = category_soup.find_all('a', class_=RECIPE_LINK_CLASS)
        except Exception as e:
            logger.error(f'failed on category URL {cl["href"]}')
            logger.error(traceback.format_exc())

            continue

        # for each recipe, use recipe_scrapers to get the recipe data and store in database
        for rl in recipe_links:
            # sleep for a random amount of time for 1 - 3 seconds so it doesn't overload the website
            sleep_time = (random() * 2) + 1
            time.sleep(sleep_time)

            try:
                logger.info(f'attempting to collect recipe with URL {rl["href"]}')
                recipe_data = scrape_recipe(rl['href'])
                save_recipe_data(recipe_data)
                logger.info(f'successfully collected recipe with URL {rl["href"]}')
                recipes_collected += 1
            except Exception as e:
                logger.error(f'failed on recipe URL {rl["href"]}')
                logger.error(traceback.format_exc())

                continue

    logger.info(f'collected {recipes_collected} recipes')

