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
        professional_installation BOOLEAN NOT NULL DEFAULT FALSE,
        product_image TEXT NOT NULL
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
        hashed_and_salted_password TEXT NOT NULL,
        admin BOOLEAN NOT NULL DEFAULT FALSE,
        salt TEXT NOT NULL
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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_date TEXT,
        order_total REAL,
        order_postcode TEXT,
        order_address TEXT,
        order_phone_number TEXT,
        order_city TEXT,
        user_email TEXT,
               
        FOREIGN KEY (user_email) REFERENCES login_details(user_email) ON DELETE CASCADE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        order_id INTEGER,
        product_id TEXT,
        product_quantity INTEGER,
        product_price REAL,
        product_professional_installation BOOLEAN,
               
        FOREIGN KEY (order_id) REFERENCES Orders(OrderID),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS delivery_info (
        user_email TEXT NOT NULL PRIMARY KEY,
        user_postcode TEXT NOT NULL,
        user_address TEXT NOT NULL,
        user_phone_number TEXT NOT NULL,
        user_city TEXT NOT NULL,

        FOREIGN KEY (user_email) REFERENCES login_details(user_email) ON DELETE CASCADE
    )
''')


# Commit the changes and close the connection
conn.commit()
conn.close()