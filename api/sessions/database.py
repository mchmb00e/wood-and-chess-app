from pymysql import connect, cursors
from dotenv import load_dotenv
from os import getenv

load_dotenv()

connection = connect(
    host = getenv("DB_HOST"),
    user = getenv("DB_USER"),
    password = getenv("DB_PASSWORD"),
    db = getenv("DB_NAME"),
    cursorclass = cursors.DictCursor
)