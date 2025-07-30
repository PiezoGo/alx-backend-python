import mysql.connector

def stream_users():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="spic3s",
        password="",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)

    # Execute query
    cursor.execute("SELECT * FROM user_data")

    # Yield each row one by one
    for row in cursor:
        yield row

    # Clean up
    cursor.close()
    conn.close()
