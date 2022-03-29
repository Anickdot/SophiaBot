import os

import dotenv
import psycopg2

dotenv.load_dotenv()


class Database:
    def __init__(self):
        connection = psycopg2.connect(
            dbname=os.environ['DB_NAME'], 
            user=os.environ['DB_USER'], 
            password=os.environ['DB_PASSWORD'], 
            host=os.environ['DB_HOST']
        )
        connection.autocommit = True
        self.cursor = connection.cursor()
