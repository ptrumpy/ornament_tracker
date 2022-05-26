import os
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

#DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file: "

load_dotenv()
database_uri = os.getenv("DATABASE_URI")

pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_uri)
