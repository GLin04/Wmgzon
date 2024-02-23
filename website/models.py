import sqlite3

# Connect to the database
conn = sqlite3.connect('wmgzon.db')
cursor = conn.cursor()

# Create the products table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
cursor.execute('''
               ''')
    

# Create the register form table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_details (
        user_email TEXT NOT NULL PRIMARY KEY,               
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        admin BOOLEAN NOT NULL DEFAULT FALSE
    )
''')

# Create the basket table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS basket (
        user_email TEXT NOT NULL,               
        product_id INTEGER NOT NULL,
        product_quantity INTEGER NOT NULL,
        professional_installation BOOLEAN NOT NULL DEFAULT FALSE,
        total_price REAL NOT NULL,
               
        FOREIGN KEY (user_email) REFERENCES login_details(user_email) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
        UNIQUE (product_id, user_email)
    )
''')


# Commit the changes and close the connection
conn.commit()
conn.close()