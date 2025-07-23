import sqlite3

# Global variable to store last column names
_last_columns = []

def run_query(query: str):
    global _last_columns
    conn = sqlite3.connect("SQL_Database/ecommerce.db")
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    # store column names
    _last_columns = [desc[0] for desc in cur.description]
    conn.close()
    return rows

def get_last_columns():
    return _last_columns
