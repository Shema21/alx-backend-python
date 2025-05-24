import time
import sqlite3
import functools
import hashlib

# Global cache dictionary
query_cache = {}

def with_db_connection(func):
    """Decorator that handles database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
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

def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    Uses SHA-256 hash of the query as the cache key.
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Create a consistent cache key by hashing the query
        cache_key = hashlib.sha256(query.encode()).hexdigest()
        
        # Check if result is already cached
        if cache_key in query_cache:
            print("Returning cached result")
            return query_cache[cache_key]
        
        # Execute and cache if not in cache
        result = func(conn, query, *args, **kwargs)
        query_cache[cache_key] = result
        print("Caching new result")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
print("First call:")
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
print("\nSecond call:")
users_again = fetch_users_with_cache(query="SELECT * FROM users")

# Verify same results
assert users == users_again