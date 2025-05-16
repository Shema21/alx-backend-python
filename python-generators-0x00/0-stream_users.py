import mysql.connector

def stream_users():
    """Generator to stream rows one by one from the user_data table."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Change this if needed
            database='ALX_prodev'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        # Single loop to yield each row one by one
        for row in cursor:
            yield row

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
