# ALX ProDev User Data Seeder

This project contains a Python script to seed a MySQL database with user data from a CSV file.

## Features

- Connects to MySQL server and creates the database `ALX_prodev` if it doesn't exist.
- Creates a table `user_data` with fields: 
  - `user_id` (UUID primary key),
  - `name` (string),
  - `email` (string, unique),
  - `age` (decimal).
- Reads user data from a CSV file and inserts it into the database.
- Avoids duplicate emails by checking before insertion.
- Provides a generator function to stream rows one by one from the database.

## Setup

1. Make sure you have MySQL installed and running on your machine.
2. Install required Python packages (if not already installed):

   ```bash
   pip install mysql-connector-python
