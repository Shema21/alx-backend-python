import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that automatically handles database connections:
    - Opens a connection before calling the function
    - Passes the connection to the decorated function
    - Closes the connection after function execution
    - Handles any potential database errors
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            # Open a new database connection
            conn = sqlite3.connect('users.db')
            
            # Call the original function with the connection
            # Pass connection as first argument if not already provided
            if 'conn' not in kwargs and not (args and isinstance(args[0], sqlite3.Connection)):
                return func(conn, *args, **kwargs)
            return func(*args, **kwargs)
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            # Ensure connection is closed
            if conn:
                conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)