import sqlite3

# Connect to the database
conn = sqlite3.connect('wmgzon.db')
cursor = conn.cursor()

# Create the products table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        stock INTEGER NOT NULL,
        productType TEXT NOT NULL,
        price REAL NOT NULL,
        deliveryTime INTEGER NOT NULL,
        brand TEXT NOT NULL,
        specifications TEXT NOT NULL,
        description TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()