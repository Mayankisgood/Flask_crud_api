import sqlite3

# Connect to the database
with sqlite3.connect('database.db') as conn:
    print("Connected to database successfully")

    # Create the Todo table with an id column, content column, and completed column
    conn.execute('''
    CREATE TABLE IF NOT EXISTS Todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        completed INTEGER NOT NULL CHECK (completed IN (0, 1))
    )
    ''')
    print("Created table successfully!")
