import os
from flask import Blueprint, app, render_template, request,redirect, session, url_for
import sqlite3
from datetime import datetime, timedelta
from flask import abort


views = Blueprint('views', __name__)




@views.route('/')
def home():
    return redirect('/electronics')


@views.route('/account')
def account():
    return render_template("account.html")


@views.route('/coming_soon')
def coming_soon():
    return render_template("coming_soon.html")


@views.route('/basket', methods=['GET', 'POST', 'PUT', 'DELETE'])
def basket():
    
    #fetch data from sessions
    user_email = session['user_email']
    
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    
    try:
        user_postcode = session.get('postcode')[0]
    except:
        return redirect('/delivery_info')

    #fetch data from the database
    cursor.execute(
        "SELECT products.*, basket.* "
        "FROM basket "
        "JOIN products ON basket.product_id = products.product_id "
        "WHERE basket.user_email = ?",
        (user_email,)
    )
    products = cursor.fetchall()
    
    #fetch the stock of the products
    product_stock = [product[2] for product in products]

    #fetch the total price of the basket
    cursor.execute('SELECT SUM(total_price) FROM basket WHERE user_email=?', (user_email,))
    total_basket_price = cursor.fetchone()[0]

    professional_installation_list = [products[15] for products in products]

    #convert the professional_installation_list to a list of strings
    for i, product in enumerate(professional_installation_list):
        if product == "true":
            professional_installation_list[i] = "Professional Installtion included (£40 per item)"
        else:
            professional_installation_list[i] = ""  
    conn.close()

    return render_template("basket.html", products=products, total_basket_price=total_basket_price, product_stock=product_stock , postcode=user_postcode, professional_installation_list=professional_installation_list)


@views.route('/add_product', methods=['GET', 'POST'])
def add_product():

    # Connect to the database
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()

    # Check if the user is an admin
    if not session['admin']:
        conn.close()
        abort(403, description="You are not authorised to access this page")

    # If the request is a GET request, return the add_product.html page
    if request.method == 'GET':
        cursor.execute('SELECT product_image FROM products')
        product_image_tuple = cursor.fetchall()
        conn.close()

        product_image_array = [item[0] for item in product_image_tuple]
        return render_template("add_product.html", product_image_array=product_image_array)

    # If the request is a POST request, insert the data into the database
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
    
    # Check if the user is an admin
    if not session['admin']:
        conn.close()
        abort(403, description="You are not authorised to access this page")

    # If the request is a GET request, return the edit_product.html page
    if request.method == 'GET':
        cursor.execute('SELECT product_image FROM products')
        product_image_tuple = cursor.fetchall()
        conn.close()

        product_image_array = [item[0] for item in product_image_tuple] 
        return render_template("edit_product.html", product_image_array=product_image_array, product=product)
    
    # If the request is a POST request, update the data in the database
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

        # If the image already exists in the folder, print a message to the console
        if os.path.exists(f'{UPLOAD_PATH}/{image.filename}'):
            print(f'{UPLOAD_PATH}/{image.filename} already exists in the folder.')
        else:
            print(f'{image.filename} uploaded successfully')
            image.save(f"{UPLOAD_PATH}/{image.filename}")

        # Update the data in the database
        cursor.execute('SELECT product_image FROM products WHERE product_id=?', (product_id,))
        product_image = cursor.fetchone()

        # If the image is the default image or the user has not uploaded a new image, keep the old image
        if product_image[0] == 'default.jpg' or image.filename == '':
            image.filename = product_image[0]
        else:
            os.remove(f"{UPLOAD_PATH}/{product_image[0]}")

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
    # If the request is a DELETE request, delete the product from the database
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

        if str(product_image[0]) != 'default.jpg':
            os.remove(f"{UPLOAD_PATH}/{product_image[0]}")

        conn.close()

        return redirect('/electronics')


@views.route('/add_to_basket', methods=['POST'])
def add_to_basket():

    try:
        user_postcode = session.get('postcode')[0]
    except:
        return redirect('/delivery_info')
    
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()

    # Check if the user is logged in and if not, redirect them to the register page
    if 'user_email' not in session:
        return redirect('/register')


    # If the request is a POST request, add the product to the basket
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        prof_installation = request.form.get('prof_installation_hidden')
        user_email = session['user_email']
        total_price = request.form.get('total_hidden')

        cursor.execute('SELECT * FROM products WHERE product_id=?', (product_id,))
        product = cursor.fetchone()

        cursor.execute('SELECT stock FROM products WHERE product_id=?', (product_id,))
        product_stock = cursor.fetchone()[0]

        cursor.execute('SELECT product_id FROM basket WHERE user_email=?', (user_email,))
        product_ids = cursor.fetchall()
        product_ids = [i[0] for i in product_ids]
        
        # Check if the there is enough stock available
        if int(quantity) > int(product_stock):
            error = "Not enough stock available. Please try again."
            return render_template("product.html", product=product, product_ids=product_ids, error=error)
        
        cursor.execute('''
            INSERT INTO basket (user_email, product_id, product_quantity, professional_installation, total_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_email, product_id, quantity, prof_installation, total_price))
        conn.commit()
        conn.close()

        return redirect(url_for('views.basket'))
    
    
@views.route('/update_basket', methods=['PUT'])
def update_basket():
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()

    # Check if the user is logged in and if not, redirect them to the register page
    if request.method == 'PUT':
        product_id = request.args.get('productId')
        quantity = request.args.get('quantity')
        total_price = request.args.get('total')
        user_email = session['user_email']

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

        cursor.execute('SELECT stock FROM products WHERE product_id=?', (product_id,))
        product_stock = cursor.fetchone()[0]

        # Check if the there is enough stock available
        if int(quantity) > int(product_stock):

            error = "Not enough stock available. Please try again."

            return render_template("basket.html", products=products, total_basket_price=total_basket_price, product_stock=product_stock, error=error)
        
        # Update the data in the database
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
    
    # If the request is a DELETE request, delete the product from the basket
    if request.method == 'DELETE':
        productId = request.args.get('productId')
        user_email = session['user_email']

        # Delete the data from the database
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()
        
        print(productId, user_email)
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

    cursor.execute('''SELECT products.deliveryTime
        FROM products
        JOIN basket ON products.product_id = basket.product_id
        WHERE basket.user_email = ?''', (user_email,))
    
    delivery_time_tuple = cursor.fetchall()
    delivery_time_list = [i[0] for i in delivery_time_tuple]

    #fetch the delivery date and convert it to a string
    current_date = datetime.now()
    current_date_str = current_date.strftime("%A, %d %B %Y")

    # Add the delivery time to the current date
    delivery_date_list = [current_date + timedelta(days=i) for i in delivery_time_list]
    formatted_delivery_date_list = [i.strftime("%A, %d %B %Y") for i in delivery_date_list]

    cursor.execute('SELECT * FROM delivery_info WHERE user_email=?', (user_email,))
    delivery_info = cursor.fetchall()[0]

    conn.close()
    
    if request.method == 'GET':
        return render_template("checkout.html", products=products, total_basket_price=total_basket_price, delivery_date=formatted_delivery_date_list, current_date=current_date_str, delivery_info=delivery_info)


@views.route('/delivery_info', methods=['GET', 'POST'])
def delivery_info():
    
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    email = session['user_email']

    # If the request is a GET request, return the delivery_info.html page
    if request.method == 'GET':

        cursor.execute('SELECT * FROM delivery_info WHERE user_email=?', (email,))
        delivery_info = cursor.fetchone()

        conn.close()
        return render_template("delivery_info.html", delivery_info=delivery_info)

    # If the request is a POST request, insert the data into the database
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
    
    # If the request is a POST request, insert the data into the database
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

        # Get the order_id of the order that was just inserted
        cursor.execute('''SELECT order_id FROM Orders WHERE(
                       order_date=? AND order_total=? AND order_postcode=? AND order_address=? AND order_phone_number=? AND order_city=? AND user_email=?)''', (current_date_time, total_basket_price, session['postcode'][0], delivery_info[2], delivery_info[3], delivery_info[4], user_email))
        order_id = cursor.fetchone()[0]

        cursor.execute('SELECT SUM(total_price) FROM basket where user_email=?', (user_email,))

        total_basket_price = cursor.fetchone()[0]

        cursor.execute('''SELECT products.deliveryTime
            FROM products
            JOIN basket ON products.product_id = basket.product_id
            WHERE basket.user_email = ?''', (user_email,))
        
        delivery_time_tuple = cursor.fetchall()
        delivery_time_list = [i[0] for i in delivery_time_tuple]

        current_date = datetime.now()
        current_date_str = current_date.strftime("%A, %d %B %Y")

        # Add the delivery time to the current date
        delivery_date_list = [current_date + timedelta(days=i) for i in delivery_time_list]
        formatted_delivery_date_list = [i.strftime("%A, %d %B %Y") for i in delivery_date_list]

        cursor.execute('SELECT * FROM delivery_info WHERE user_email=?', (user_email,))
        delivery_info = cursor.fetchall()[0]

        # Update the stock of the products in the database
        for product in purchased_products:
   
            product_id = product[0]
            product_quantity_purchased = product[14]

            cursor.execute('SELECT stock FROM products WHERE product_id=?', (product_id,))
            current_stock = cursor.fetchone()[0]
            updated_stock = current_stock - product_quantity_purchased

            cursor.execute('UPDATE products SET stock=? WHERE product_id=?', (updated_stock, product_id))

            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, product_quantity, product_price, product_professional_installation)
                VALUES (?, ?, ?, ?, ?)
            ''', (order_id, product_id, product_quantity_purchased, product[4], product[15]))

        # Delete the products from the user basket
        cursor.execute('DELETE FROM basket WHERE user_email=?', (user_email,))

        conn.commit()
        conn.close()

        return render_template("order_confirmation.html", purchased_products=purchased_products, current_date_str=current_date_str, delivery_date=formatted_delivery_date_list, delivery_info=delivery_info, total_basket_price=total_basket_price)
    
    
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

    # renders the orders.html page with the orders data
    return render_template("orders.html", orders=orders)


@views.route('/contact')
def contact():
    return render_template("contact.html")

@views.route('/email_sent')
def email_sent():
    return render_template("email_sent.html")

@views.route('/contact_it')
def contact_it():
    return render_template("contact_it.html")