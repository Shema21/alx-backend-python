import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that fetches rows from user_data in batches of batch_size."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # adjust if needed
            database='ALX_prodev'
        )
        cursor = conn.cursor(dictionary=True)
        offset = 0

        while True:
            cursor.execute(
                "SELECT * FROM user_data ORDER BY user_id LIMIT %s OFFSET %s",
                (batch_size, offset)
            batch = cursor.fetchall()
            if not batch:
                cursor.close()
                conn.close()
                return  # Explicit return when done
            yield batch
            offset += batch_size

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return  

def batch_processing(batch_size):
    """Process batches by filtering users with age > 25, yield filtered users."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
    return 
