"""

Takes JSON files from data/ and loads them to the cookit database

"""

import json
import logging
import os
import psycopg2
import traceback
from utils.decorators import time_function


LOADED_FILES_LOG = "files_loaded.txt"

def load_secrets():
    with open("secrets.json") as secrets_file:
        secrets = json.load(secrets_file)

    return secrets

# retrieve the list of files that have already been loaded to the db from data/files_loaded.txt
def get_loaded_files() -> list[str]:
    # if file doesn't exist, nothing has been loaded yet
    if not os.path.exists(f"logs/{LOADED_FILES_LOG}"):
        return []
    
    with open(f"logs/{LOADED_FILES_LOG}") as f:
        lines = f.readlines()

    lines = [line.replace("\n", "") for line in lines]
    return lines

def insert_to_tables(data: dict, conn):
    cur = conn.cursor()

    # note that for all string fields, ' is escaped with ''
    # None also needs to be translated to null

    title = "'" + data["title"].replace("'", "''") + "'"
    image = "'" + data["image"].replace("'", "''") + "'" if data["image"] else 'null'
    prep_time = data['prep_time'] if data['prep_time'] else 'null'
    cook_time = data['cook_time'] if data['cook_time'] else 'null'
    total_time = data['total_time'] if data['total_time'] else 'null'
    yields = "'" + data["yields"].replace("'", "''") + "'" if data["yields"] else 'null'
    cuisine = "'" + data["cuisine"].replace("'", "''") + "'" if data["cuisine"] else 'null'
    category = "'" + data["category"].replace("'", "''") + "'" if data["category"] else 'null'

    cur.execute(f"""
        insert into cookit_recipe (name, prep_time, cook_time, total_time, image, yields, cuisine, category) values
        (
            {title}, 
            {prep_time}, 
            {cook_time}, 
            {total_time}, 
            {image}, 
            {yields}, 
            {cuisine},
            {category}
        )
        returning id;
    """)

    recipe_id = cur.fetchone()[0]

    for ingredient in data['ingredients']:
        cur.execute(f"""
            insert into cookit_recipeingredient (recipe_id, ingredient) values
            ({recipe_id}, '{ingredient.replace("'", "''")}')
        """)

    for i, instruction in enumerate(data['instructions_list']):
        step_no = i + 1

        cur.execute(f"""
            insert into cookit_recipeinstruction (recipe_id, step_no, instruction) values
            ({recipe_id}, {step_no}, '{instruction.replace("'", "''")}')
        """)

    for nutrient, quantity in data['nutrients'].items():
        cur.execute(f"""
            insert into cookit_recipenutrition (recipe_id, nutrient, quantity) values
            ({recipe_id}, '{nutrient.replace("'", "''")}', '{quantity.replace("'", "''")}')
        """)

    conn.commit()

@time_function
def load_files_to_db():
    secrets = load_secrets()
    logger = logging.getLogger('cookit-scraper')
    loaded_files = get_loaded_files()

    conn = psycopg2.connect(
        database=secrets['postgres_db'],
        user=secrets['postgres_user'],
        password=secrets['postgres_password'],
        host=secrets['postgres_host'],
        port=secrets['postgres_port']
    )

    # get files that have not already been loaded, make sure we only grab json files
    data_files = os.listdir('data')
    data_files = [file for file in data_files if file not in loaded_files and file.endswith(".json")]

    for file in data_files:
        try:
            with open(f"data/{file}") as f:
                data = json.load(f)
        except:
            logger.error(f"failed to read JSON from file {file}")
            logger.error(traceback.format_exc())
            continue

        try:
            insert_to_tables(data, conn)
            with open(f"logs/{LOADED_FILES_LOG}", "a") as f:
                f.write(f"{file}\n")

            logger.info(f"successfully loaded file {file}")
        except:
            logger.error(f"failed to load file {file}")
            logger.error(traceback.format_exc())
            conn.rollback()
    
    conn.close()
