import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        # Open DB connection and create cursor
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        
        # Execute the query with optional parameters
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()  # Fetch results
        
        return self.result  # Returned to the `as` variable in `with`

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup: close cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
