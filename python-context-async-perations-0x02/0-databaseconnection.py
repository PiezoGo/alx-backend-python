import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # makes the connection object available in the `with` block

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()  # automatically closes connection
        if exc_type:
            print(f"[ERROR] {exc_type.__name__}: {exc_value}")
        return False  # propagate exception if any

# ✅ Use the context manager
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)
