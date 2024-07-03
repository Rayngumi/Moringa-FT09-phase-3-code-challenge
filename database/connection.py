import sqlite3

DATABASE_NAME = './database/magazine.db'

def get_db_connection():
    CONN = sqlite3.connect(DATABASE_NAME)
    CONN.row_factory = sqlite3.Row
    return CONN