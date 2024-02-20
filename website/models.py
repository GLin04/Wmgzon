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
        description TEXT NOT NULL,
        professional_installation BOOLEAN NOT NULL DEFAULT FALSE
    )
''')

# In case i need to edit a table
# cursor.execute('''
#     ALTER TABLE products
#     ADD COLUMN professional_installation BOOLEAN NOT NULL DEFAULT FALSE
#                ''')

# Create the register form table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_details (
        email TEXT NOT NULL PRIMARY KEY,               
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        admin BOOLEAN NOT NULL DEFAULT FALSE
    )
''')

# Create the basket table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS basket (
        email TEXT NOT NULL PRIMARY KEY,               
        productid INTEGER NOT NULL,
        product_quantity INTEGER NOT NULL,
        professional_installation BOOLEAN NOT NULL DEFAULT FALSE
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()