import mysql.connector

def stream_user_ages():
    """Generator to yield user ages one by one from the DB"""
    conn = mysql.connector.connect(
        host="localhost",
        user="spic3s",
        password="Piezo55Go!.",
        database="ALX_prodev"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # Loop 1
        yield age

    cursor.close()
    conn.close()


def compute_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():  # Loop 2
        total += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        print(f"Average age of users: {total / count:.2f}")


if __name__ == "__main__":
    compute_average_age()
