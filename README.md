# cookit-scraper

To load data to a local DB, requires <a href="https://github.com/MarkyMan4/cookit-api" target="_blank">cookit-api</a> to be checked out 
and the Postgres container running to use as the local database.

Create a file called `secrets.json` at the root of this repo and include the following information about the database connection:

```json
{
    "postgres_db": "<db>",
    "postgres_user": "<user>",
    "postgres_password": "<password>",
    "postgres_host": "<host>",
    "postgres_port": "<port>"
}
```
