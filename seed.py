import csv
import mysql.connector
from mysql.connector import errorcode
import uuid

# 1. Connect to MySQL Server
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",
        password="your_mysql_password"
    )

# 2. Create the database if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("[✔] Database 'ALX_prodev' ensured.")
    finally:
        cursor.close()

# 3. Connect directly to ALX_prodev
def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",
        password="your_mysql_password",
        database="ALX_prodev"
    )

# 4. Create user_data table with UUID primary key
def create_table(connection):
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        age DECIMAL NOT NULL,
        UNIQUE KEY (email)
    )
    """
    try:
        cursor.execute(query)
        print("[✔] Table 'user_data' ensured.")
    finally:
        cursor.close()

# 5. Insert data if it does not already exist
def insert_data(connection, data):
    cursor = connection.cursor()
    insert_query = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    try:
        for row in data:
            user_id = str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = row['age']
            cursor.execute(insert_query, (user_id, name, email, age))
        connection.commit()
        print(f"[✔] Inserted {cursor.rowcount} new rows.")
    finally:
        cursor.close()

# 6. Load data from CSV
def load_csv(file_path):
    with open(file_path, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

# 7. Main function
def main():
    try:
        # Step 1: Connect to MySQL server
        connection = connect_db()
        create_database(connection)
        connection.close()

        # Step 2: Connect to ALX_prodev
        connection = connect_to_prodev()
        create_table(connection)

        # Step 3: Load data from CSV
        data = load_csv("user_data.csv")

        # Step 4: Insert into DB
        insert_data(connection, data)

        connection.close()

    except mysql.connector.Error as err:
        print(f"[✘] MySQL Error: {err}")
    except Exception as e:
        print(f"[✘] Error: {e}")

if __name__ == "__main__":
    main()
