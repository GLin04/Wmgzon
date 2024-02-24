import os
from flask import Blueprint, app, render_template, request,redirect, session, url_for
import sqlite3

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/account')
def account():
    return render_template("account.html")

@views.route('/coming_soon')
def coming_soon():
    return render_template("coming_soon.html")

@views.route('/basket', methods=['GET', 'POST', 'PUT', 'DELETE'])
def basket():
    
    user_email = session['user_email']

    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()


    cursor.execute(
        "SELECT products.*, basket.* "
        "FROM basket "
        "JOIN products ON basket.product_id = products.product_id "
        "WHERE basket.user_email = ?",
        (user_email,)
    )

    products = cursor.fetchall()
    
    cursor.execute('SELECT SUM(total_price) FROM basket')

    total_basket_price = cursor.fetchone()[0]
    
    conn.close()



    return render_template("basket.html", products=products, total_basket_price=total_basket_price)

@views.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method=='POST':

        # Connect to the database
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()

        # Get the data from the HTML form
        name = str(request.form['name'])
        stock = int(request.form['stock'])
        product_type = str(request.form['productType'])
        price = float(request.form['price'])
        delivery_time = int(request.form['deliveryTime'])
        brand = str(request.form['brand'])
        specifications = str(request.form['specifications'])
        description = str(request.form['description'])
        image = request.files['inputFile']

        UPLOAD_PATH = 'website/static/images'
        
        if os.path.exists(f'{UPLOAD_PATH}/{image.filename}'):
            print(f'{UPLOAD_PATH}/{image.filename} already exists in the folder.')
        else:
            print(f'{image.filename} uploaded successfully')
            image.save(f"{UPLOAD_PATH}/{image.filename}")



        # Insert the data into the database
        cursor.execute('''
            INSERT INTO products (name, stock, productType, price, deliveryTime, brand, specifications, description, product_image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, stock, product_type, price, delivery_time, brand, specifications, description, image.filename))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

    return render_template("add_product.html")

@views.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        # Get the data from the HTML form
        name = str(request.form['name'])
        stock = int(request.form['stock'])
        product_type = str(request.form['productType'])
        price = float(request.form['price'])
        delivery_time = int(request.form['deliveryTime'])
        brand = str(request.form['brand'])
        specifications = str(request.form['specifications'])
        description = str(request.form['description'])

        # Update the product in the database
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()
        update_sql = '''
            UPDATE products 
            SET name=?, 
                stock=?, 
                productType=?, 
                price=?, 
                deliveryTime=?, 
                brand=?, 
                specifications=?, 
                description=? 
            WHERE product_id=?
        '''
        cursor.execute(update_sql, (
            name, stock, product_type, price, delivery_time, brand, specifications, description, product_id))
        conn.commit()
        conn.close()

        return redirect(url_for('electronics.products'))

    # Fetch the product data from the database
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE product_id=?', (product_id,))
    product = cursor.fetchone()
    conn.close()

    return render_template("edit_product.html", product=product)

@views.route('/delete_product/<int:product_id>' , methods=['DELETE'])
def delete_product(product_id):
    if request.method == 'DELETE':
        # Delete the product from the database
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE product_id=?', (product_id,))
        conn.commit()
        conn.close()

        return

@views.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        prof_installation = request.form.get('prof_installation_hidden')
        user_email = session['user_email']
        total_price = request.form.get('total_hidden')

        # Insert the data into the database
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO basket (user_email, product_id, product_quantity, professional_installation, total_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_email, product_id, quantity, prof_installation, total_price))
        conn.commit()
        conn.close()

        return redirect(url_for('views.basket'))
    
@views.route('/update_basket', methods=['PUT'])
def update_basket():
    if request.method == 'PUT':
        product_id = request.args.get('productId')
        quantity = request.args.get('quantity')
        total_price = request.args.get('total')
        user_email = session['user_email']

        # Update the data in the database
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE basket
            SET product_quantity=?, total_price=?
            WHERE user_email=? AND product_id=?
        ''', (quantity, total_price, user_email, product_id))
        conn.commit()
        conn.close()

        return redirect(url_for('views.basket'))
    
@views.route('/delete_basket', methods=['DELETE'])
def delete_from_basket():
    if request.method == 'DELETE':
        productId = request.args.get('productId')
        user_email = session['user_email']

        # Delete the data from the database
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM basket
            WHERE user_email=? AND product_id=?
        ''', (user_email, productId))
        conn.commit()
        conn.close()

        return redirect(url_for('views.basket'))
    
        