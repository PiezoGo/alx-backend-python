import mysql.connector

def paginate_users(page_size, offset):
    """Fetch a single page of users from the database"""
    conn = mysql.connector.connect(
        host="localhost",
        user="spic3s",
        password="Piezo55Go!.",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def lazy_paginate(page_size):
    """Generator that lazily paginates users using one loop"""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
