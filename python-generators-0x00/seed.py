import mysql.connector
import csv
import uuid

# 1. Connect to MySQL server
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )

# 2. Create database if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

# 3. Connect to the ALX_prodev database
def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="ALX_prodev"
    )

# 4. Create user_data table
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX(user_id)
        )
    """)
    cursor.close()

# 5. Insert data if not already present
def insert_data(connection, data):
    cursor = connection.cursor()

    for row in data:
        name, email, age = row
        # Check if this email already exists to avoid duplicates
        cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
        if cursor.fetchone() is None:
            user_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (user_id, name, email, float(age))
            )

    connection.commit()
    cursor.close()

# 6. Load CSV data
def load_csv_data(filename):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return list(reader)

# 7. Run everything
if __name__ == "__main__":
    # Connect to server and create database
    server_conn = connect_db()
    create_database(server_conn)
    server_conn.close()

    # Connect to ALX_prodev DB
    db_conn = connect_to_prodev()
    create_table(db_conn)

    # Load and insert CSV data
    csv_data = load_csv_data('user_data.csv')
    insert_data(db_conn, csv_data)

    db_conn.close()
    print("✅ Done: Database seeded successfully.")
