from database.connection import get_db_connection

CONN = get_db_connection()
CURSOR = CONN.cursor()
