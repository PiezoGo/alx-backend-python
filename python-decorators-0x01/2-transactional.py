import sqlite3 
import functools

## here is some dummy data iserted nto the table
# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT NOT NULL
# )
# ''')

# # Insert some sample users
# cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
# cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")

# conn.commit()
# # conn.close()

# print("✅ users table created and data inserted.")
## end of quote


"""your code goes here"""
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try: 
            result = func(conn,*args,**kwargs)
        finally:
            cursor.close()
        return result
    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn,*args,**kwargs):
        try:
            result = func(conn,*args,**kwargs)
            conn.commit()
        except:
            conn.rollback()
            print(f"[ERROR] Transaction failed: {e}")
            raise
        return result
    return wrapper


@with_db_connection
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
