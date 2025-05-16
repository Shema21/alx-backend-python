import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

def connect_db():
    """Connect to MySQL server (no default DB)."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='', 
            database='ALX_prodev'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Create user_data table with user_id(UUID), name, email, age."""
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                UNIQUE KEY email_unique (email),
                INDEX user_id_index (user_id)
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    cursor.close()

def insert_data(connection, csv_file):
    """Insert CSV data into user_data table if email doesn't exist."""
    cursor = connection.cursor()
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if email exists to avoid duplicates
            cursor.execute("SELECT 1 FROM user_data WHERE email = %s LIMIT 1", (row['email'],))
            if cursor.fetchone():
                continue
            # Generate UUID for user_id
            user_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, row['name'], row['email'], row['age']))
        connection.commit()
    cursor.close()

def stream_user_data(connection):
    """Generator that yields rows one by one from user_data."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()

connection = connect_to_prodev()
if connection:
    create_table(connection)
    insert_data(connection, 'user_data.csv') 
