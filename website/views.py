import os
from flask import Blueprint, app, render_template, request,redirect, session, url_for
import sqlite3
from datetime import datetime


views = Blueprint('views', __name__)


# def base():
#     conn = sqlite3.connect('wmgzon.db')
#     cursor = conn.cursor()
#     user_email = session['user_email']

#     delivery_info = cursor.execute('SELECT * FROM delivery_info WHERE user_email=?', (user_email,)).fetchone()

#     # Execute a query to search for products based on a keyword
#     cursor.execute('''
#         SELECT * FROM products
#         WHERE name LIKE ?
#         OR productType LIKE ?
#         OR brand LIKE ?
#     ''', ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))

#     # Fetch the results
#     results = cursor.fetchall()
#     print("hi")
#     # Process the results
#     for row in results:
#         # Process each row as needed
#         print(row)


#     conn.commit()
#     conn.close()

#     return render_template("base.html" , delivery_info=delivery_info)

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
    
    cursor.execute('SELECT SUM(total_price) FROM basket WHERE user_email=?', (user_email,))

    total_basket_price = cursor.fetchone()[0]
    
    conn.close()



    return render_template("basket.html", products=products, total_basket_price=total_basket_price)

@views.route('/add_product', methods=['GET', 'POST'])
def add_product():

    # Connect to the database
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('SELECT product_image FROM products')
        product_image_tuple = cursor.fetchall()
        conn.close()

        product_image_array = [item[0] for item in product_image_tuple]
        print(product_image_array)
        return render_template("add_product.html", product_image_array=product_image_array)

    
    elif request.method=='POST':

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
            INSERT INTO products (
                       name, 
                       stock, 
                       productType, 
                       price, 
                       deliveryTime, 
                       brand, 
                       specifications, 
                       description, 
                       product_image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, stock, product_type, price, delivery_time, brand, specifications, description, image.filename))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        return redirect('/electronics')



@views.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):

    # Connect to the database
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM products WHERE product_id=?', (product_id,))
    product = cursor.fetchone()
    
    if request.method == 'GET':
        cursor.execute('SELECT product_image FROM products')
        product_image_tuple = cursor.fetchall()
        conn.close()

        product_image_array = [item[0] for item in product_image_tuple] 
        return render_template("edit_product.html", product_image_array=product_image_array, product=product)
    
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
        image = request.files['inputFile']
        UPLOAD_PATH = 'website/static/images'

        if os.path.exists(f'{UPLOAD_PATH}/{image.filename}'):
            print(f'{UPLOAD_PATH}/{image.filename} already exists in the folder.')
        else:
            print(f'{image.filename} uploaded successfully')
            image.save(f"{UPLOAD_PATH}/{image.filename}")

        cursor.execute('SELECT product_image FROM products WHERE product_id=?', (product_id,))
        product_image = cursor.fetchone()

        if product_image[0] == 'default.jpg' or image.filename == '':
            print('Default image or no change detected. No need to delete')
            image.filename = product_image[0]
        else:
            os.remove(f"{UPLOAD_PATH}/{product_image[0]}")
            print(f'File {UPLOAD_PATH}/{product_image[0]} deleted successfully')

        update_sql = '''
            UPDATE products 
            SET name=?, 
                stock=?, 
                productType=?, 
                price=?, 
                deliveryTime=?, 
                brand=?, 
                specifications=?, 
                description=?, 
                product_image=?
            WHERE product_id=?
        '''
        cursor.execute(update_sql, (
            name, stock, product_type, price, delivery_time, brand, specifications, description, image.filename, product_id))
        conn.commit()
        conn.close()

        return redirect('/electronics')

    conn.close()

    return render_template("edit_product.html", product=product)

@views.route('/delete_product/<int:product_id>' , methods=['DELETE'])
def delete_product(product_id):
    if request.method == 'DELETE':
        UPLOAD_PATH = 'website/static/images'
        # Delete the product from the database
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()

        
        cursor.execute('SELECT product_image FROM products WHERE product_id=?', (product_id,))
        product_image = cursor.fetchone()

        # Delete the product from the database
        cursor.execute('DELETE FROM products WHERE product_id=?', (product_id,))
        conn.commit()


        os.remove(f"{UPLOAD_PATH}/{product_image[0]}")

        conn.close()

        return redirect('/electronics')

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
    
@views.route('/checkout' , methods=['GET', 'POST'])
def checkout():

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
    
    cursor.execute('SELECT SUM(total_price) FROM basket where user_email=?', (user_email,))

    total_basket_price = cursor.fetchone()[0]
    
    conn.close()

    if request.method == 'GET':
        return render_template("checkout.html", products=products, total_basket_price=total_basket_price)

@views.route('/delivery_info', methods=['GET', 'POST'])
def delivery_info():
    
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    email = session['user_email']

    if request.method == 'GET':

        cursor.execute('SELECT * FROM delivery_info WHERE user_email=?', (email,))
        delivery_info = cursor.fetchone()

        conn.close()
        return render_template("delivery_info.html", delivery_info=delivery_info)

    if request.method == 'POST':
        postcode = request.form['postcode']
        address = request.form['address']
        city = request.form['city']
        phone = request.form['phone_number']

        session['postcode'] = postcode


        cursor.execute('SELECT user_email FROM delivery_info WHERE user_email=?', (email,))
        existing_email = cursor.fetchone()

        if existing_email:
            cursor.execute('''
                UPDATE delivery_info
                SET user_postcode=?, user_address=?, user_phone_number=?, user_city=?
                WHERE user_email=?
                ''', (postcode, address, phone, city, email)
            )
        else:
            cursor.execute('''
                INSERT INTO delivery_info (user_email, user_postcode, user_address, user_phone_number, user_city)
                VALUES (?, ?, ?, ?, ?)
                ''', (email, postcode, address, phone, city)
            )
            

        conn.commit()
        conn.close()

        return redirect('/account')

    return render_template("delivery_info.html")    
    
@views.route('/order_confirmation', methods=['POST'])
def order_confirmation():
    if request.method == 'POST':
        user_email = session['user_email']
        current_date_time = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT products.*, basket.* "
            "FROM basket "
            "JOIN products ON basket.product_id = products.product_id "
            "WHERE basket.user_email = ?",
            (user_email,)
        )

        purchased_products = cursor.fetchall()
        
        cursor.execute('SELECT SUM(total_price) FROM basket where user_email=?', (user_email,))
        total_basket_price = cursor.fetchone()[0]

        cursor.execute('SELECT * FROM delivery_info WHERE user_email=?', (user_email,))
        delivery_info = cursor.fetchone()
        
        cursor.execute('''
            INSERT INTO orders (
                order_date,
                order_total,
                order_postcode,
                order_address,
                order_phone_number,
                order_city,
                user_email
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (current_date_time, total_basket_price, session['postcode'][0], delivery_info[2], delivery_info[3], delivery_info[4], user_email))

        cursor.execute('SELECT order_id FROM Orders WHERE user_email=?', (user_email,))
        order_id = cursor.fetchone()[0]

        for product in purchased_products:
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, product_quantity, product_price, product_professional_installation)
                VALUES (?, ?, ?, ?, ?)
            ''', (order_id, product[0], product[13], product[4], product[14]))
        
        cursor.execute('DELETE FROM basket WHERE user_email=?', (user_email,))

        conn.commit()
        conn.close()

        return render_template("order_confirmation.html", purchased_products=purchased_products)
    
@views.route('/orders')
def orders():
    user_email = session['user_email']

    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT orders.*, order_items.*, products.*
        FROM orders
        JOIN order_items ON orders.order_id = order_items.order_id
        JOIN products ON order_items.product_id = products.product_id
        WHERE orders.user_email=?
    ''', (user_email,))

    orders = cursor.fetchall()
    conn.close()

    return render_template("orders.html", orders=orders)

@views.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':

        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        user_email = session['user_email']

        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()

        cursor.execute('SELECT password FROM login_details WHERE email=?', (user_email,))
        current_password = cursor.fetchone()[0]

        if old_password == current_password and new_password == confirm_password:
            cursor.execute('UPDATE login_details SET password=? WHERE email=?', (new_password, user_email))
            conn.commit()
            conn.close()
            return redirect('/account')
        else:
            conn.close()
            return render_template("change_password.html", error="Invalid password or passwords do not match")

    return render_template("change_password.html")