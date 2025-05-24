import sqlite3

class ExecuteQuery:
    """Custom context manager for executing parameterized queries."""
    
    def __init__(self, query, params=None, db_name='users.db'):
        self.query = query
        self.params = params if params is not None else ()
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        """Execute the query when entering context."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting context."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Return False to propagate any exceptions
        return False

# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    
    try:
        with ExecuteQuery(query, params) as cursor:
            results = cursor.fetchall()
            print("Users over 25 years old:")
            for row in results:
                print(row)
                
    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")