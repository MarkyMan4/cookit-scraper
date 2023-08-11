from recipe_scrapers import scrape_me


def main():
    scraper = scrape_me('https://www.allrecipes.com/parmesan-chive-biscuits-recipe-7505885')
    
    print(f'host: {scraper.host()}\n')
    print(f'title: {scraper.title()}\n')
    print(f'total_time: {scraper.total_time()}\n')
    print(f'image: {scraper.image()}\n')
    print(f'ingredients: {scraper.ingredients()}\n')
    print(f'ingredient_groups: {scraper.ingredient_groups()}\n')
    print(f'instructions: {scraper.instructions()}\n')
    print(f'instructions_list: {scraper.instructions_list()}\n')
    print(f'yields: {scraper.yields()}\n')
    print(f'nutrients: {scraper.nutrients()}\n')
    print(f'cuisine: {scraper.cuisine()}\n')
    print(f'category: {scraper.category()}\n')
    print(f'prep_time: {scraper.prep_time()}\n')
    print(f'cook_time: {scraper.cook_time()}\n')

if __name__ == '__main__':
    main()

