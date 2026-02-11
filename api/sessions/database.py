from pymysql import connect, cursors
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# En vez de crear la conexión aquí, definimos una función
def get_db_connection():
    return connect(
        host = getenv("DB_HOST"),
        user = getenv("DB_USER"),
        password = getenv("DB_PASSWORD"),
        db = getenv("DB_NAME"),
        cursorclass = cursors.DictCursor
    )