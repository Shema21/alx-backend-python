import time
import sqlite3
import functools
from random import random

def with_db_connection(func):
    """
    Decorator that automatically handles database connections.
    Opens a connection before calling the function and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            # Pass connection as first argument if not already provided
            if 'conn' not in kwargs and not (args and isinstance(args[0], sqlite3.Connection)):
                return func(conn, *args, **kwargs)
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries the function if it fails.
    Args:
        retries: Number of retry attempts
        delay: Initial delay between retries in seconds (will increase with jitter)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries + 1):  # +1 for the initial attempt
                try:
                    return func(*args, **kwargs)
                except (sqlite3.Error, sqlite3.OperationalError) as e:
                    last_exception = e
                    if attempt < retries:
                        # Calculate wait time with jitter to avoid thundering herd
                        wait_time = delay * (1 + 0.1 * random())  # Add 10% jitter
                        print(f"Attempt {attempt + 1} failed. Retrying in {wait_time:.2f} seconds...")
                        time.sleep(wait_time)
            print(f"All {retries} retry attempts failed")
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)