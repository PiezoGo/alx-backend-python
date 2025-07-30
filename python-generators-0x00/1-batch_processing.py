import mysql.connector

def stream_users_in_batches(batch_size):
    conn = mysql.connector.connect(
        host="localhost",
        user="spic3s",
        password="",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)

    offset = 0
    while True:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    cursor.close()
    conn.close()
    return  # <-- Proper use of return in a generator (to end it)


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):  # 1st loop
        filtered_batch = [user for user in batch if user["age"] > 25]  # 2nd loop
        for user in filtered_batch:  # 3rd loop
            yield user
    return  # <-- Ends generator explicitly
