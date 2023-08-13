import json
import requests
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_me


CATEGORY_PAGE_URL = 'https://www.allrecipes.com/recipes-a-z-6735880'
CATEGORY_LINK_CLASS = 'link-list__link'
RECIPE_LINK_CLASS = 'comp mntl-card-list-items mntl-document-card mntl-card card card--no-image'

def scrape_recipe(url: str) -> dict:
    scraper = scrape_me(url)
    
    recipe_data = {
        'host': scraper.host(),
        'title': scraper.title(),
        'total_time': scraper.total_time(),
        'image': scraper.image(),
        'ingredients': scraper.ingredients(),
        'instructions': scraper.instructions(),
        'instructions_list': scraper.instructions_list(),
        'yields': scraper.yields(),
        'nutrients': scraper.nutrients(),
        'cuisine': scraper.cuisine(),
        'category': scraper.category(),
        'prep_time': scraper.prep_time(),
        'cook_time': scraper.cook_time(),
    }

    return recipe_data

# TODO: this will write to database, for now just saving to files
def save_recipe_data(recipe_data: dict):
    file_name = recipe_data['title'].lower().replace(' ', '_') + '.json'
    
    with open(f'data/{file_name}', 'w') as f:
        json.dump(recipe_data, f)

def make_soup(url: str) -> BeautifulSoup:
    res = requests.get(url)
    return BeautifulSoup(res.text)

def main():
    soup = make_soup(CATEGORY_PAGE_URL)
    category_links = soup.find_all('a', class_=CATEGORY_LINK_CLASS)

    # initial page is categories, each category has links to actual recipes
    # scrape each category link for links to recipes
    for cl in category_links:
        category_soup = make_soup(cl['href'])
        recipe_links = category_soup.find_all('a', class_=RECIPE_LINK_CLASS)

        # for each recipe, use recipe_scrapers to get the recipe data and store in database
        for rl in recipe_links:
            recipe_data = scrape_recipe(rl['href'])
            save_recipe_data(recipe_data)


if __name__ == '__main__':
    main()

