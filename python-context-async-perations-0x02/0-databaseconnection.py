import sqlite3

class DatabaseConnection:
    """Custom context manager for SQLite database connections."""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
    
    def __enter__(self):
        """Open database connection when entering context."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection when exiting context."""
        if self.conn:
            self.conn.close()
        # Return False to propagate any exceptions
        return False

# Example usage with the context manager
if __name__ == "__main__":
    db_name = "users.db"
    
    try:
        with DatabaseConnection(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            
            # Print the results
            print("Query Results:")
            for row in results:
                print(row)
                
    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")