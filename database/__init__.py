from database.connection import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()