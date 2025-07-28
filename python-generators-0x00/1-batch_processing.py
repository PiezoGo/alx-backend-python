import mysql.connector

def stream_users_in_batches(batch_size):
    conn = mysql.connector.connect(
        host="localhost",
        user="spic3s",
        password="Piezo55Go!.",
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


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):  # 1st loop
        filtered_batch = [user for user in batch if user["age"] > 25]  # 2nd loop (list comprehension)
        for user in filtered_batch:  # 3rd loop
            yield user
