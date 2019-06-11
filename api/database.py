from os import environ
import psycopg2
from dotenv import load_dotenv

if "ENV" not in environ or environ["ENV"] == "development":
    print("Loading ENV VARS from .env")
    load_dotenv()


def init_db_connection():
    pg_user = environ["POSTGRES_USER"]
    pg_pass = environ["POSTGRES_PASSWORD"]
    pg_host = environ["POSTGRES_HOST"]
    pg_port = environ["POSTGRES_PORT"]
    connection = None

    try:
        connection = psycopg2.connect(
            dbname="postgres",
            host=pg_host,
            port=pg_port,
            user=pg_user,
            password=pg_pass
        )
    except psycopg2.Error:
        print("Error: Unable to connection to database")
        print("ENV: %s" % environ)
        exit(1)

    return connection


postgres_connection = init_db_connection()
