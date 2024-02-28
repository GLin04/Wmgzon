from flask import Blueprint, redirect, render_template, request, session
import sqlite3
electronics = Blueprint('electronics', __name__)

@electronics.route('/' , methods=['GET', 'POST'])
def products():


    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    if request.method == 'GET':
        conn.close()
        return render_template("electronics.html", products=products)
    
    elif request.method == 'POST':
        filter_list = []
        filter_list += request.form.getlist('accessories_filter')
        filter_list += request.form.getlist('data_storage_filter')
        filter_list += request.form.getlist('desktop_filter')
        filter_list += request.form.getlist('laptop_filter')
        filter_list += request.form.getlist('monitor_filter')
        filter_list += request.form.getlist('phone_filter')
        filter_list += request.form.getlist('printer_filter')
        filter_list += request.form.getlist('tv_filter')
        max_price = request.form['max_price']

        if len(filter_list) == 0:
            cursor.execute('SELECT * FROM products')
            filter_only_products = cursor.fetchall()
        else:
            get_filter_products = '''
                SELECT * FROM products
                WHERE productType IN ({})
            '''.format(','.join(['?'] * len(filter_list)))

            cursor.execute(get_filter_products, filter_list)
            filter_only_products = cursor.fetchall()
        
        cursor.execute('''SELECT * FROM products
                    WHERE price <= ?''', (max_price,))

        max_price_products = cursor.fetchall()

        filtered_products = [product for product in max_price_products if product in filter_only_products]



        conn.close()
        return render_template("electronics.html", products=filtered_products , filter_list=filter_list)
    

@electronics.route('/product/<int:product_id>')
def product(product_id):
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    user_email = session['user_email']

    cursor.execute("SELECT * FROM products WHERE product_id=?", (product_id,))
    product = cursor.fetchone()

    cursor.execute('SELECT product_id FROM basket WHERE user_email=?', (user_email,))

    product_ids = cursor.fetchall()
    product_ids = [i[0] for i in product_ids]

    # close the connection
    conn.close()

    # render the template with the product details
    return render_template("product.html", product=product, product_ids=product_ids, error='')



@electronics.route('/search', methods=['POST', 'GET'])
def search():
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()

    try:
        session['search_input'] = request.form['search_input']
        search_input = session['search_input']
    except:
        session['search_input'] = ''
        search_input = session['search_input']


    if request.method == 'GET':
        
        cursor.execute('SELECT * FROM products')
        filtered_products = cursor.fetchall()
        conn.close()
        return render_template('search_results.html', search_input=search_input, filtered_products=filtered_products)
    
    if request.method == 'POST':



        filter_list = []
        filter_list += request.form.getlist('accessories_filter')
        filter_list += request.form.getlist('data_storage_filter')
        filter_list += request.form.getlist('desktop_filter')
        filter_list += request.form.getlist('laptop_filter')
        filter_list += request.form.getlist('monitor_filter')
        filter_list += request.form.getlist('phone_filter')
        filter_list += request.form.getlist('printer_filter')
        filter_list += request.form.getlist('tv_filter')

        try:
            max_price = request.form['max_price']
        except:
            max_price = 1000000

        cursor.execute('''
            SELECT * FROM products
            WHERE name LIKE ?
        ''', ('%' + search_input + '%',))

        searched_products = cursor.fetchall()

        if len(filter_list) == 0:
            cursor.execute('SELECT * FROM products')
            filter_only_products = cursor.fetchall()
        else:
            get_filter_products = '''
                SELECT * FROM products
                WHERE productType IN ({})
            '''.format(','.join(['?'] * len(filter_list)))

            cursor.execute(get_filter_products, filter_list)
            filter_only_products = cursor.fetchall()

        cursor.execute('''SELECT * FROM products
                    WHERE price <= ?''', (max_price,))

        max_price_products = cursor.fetchall()

        
        searched_filtered_products = [product for product in searched_products if product in filter_only_products]

        filtered_products = [product for product in searched_filtered_products if product in max_price_products]



        conn.close()
        return render_template('search_results.html', filtered_products=filtered_products, search_input=search_input, filter_list=filter_list)
    
@electronics.route('/add_review', methods=['POST'])
def add_review():
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()

    product_id = request.form['product_id']
    rating = request.form['rating']

    cursor.execute('''
        INSERT INTO product_reviews (product_id, rating)
        VALUES (?, ?)
    ''', (product_id, rating))

    average_rating_query = '''
        SELECT AVG(rating) FROM product_reviews
        WHERE product_id = ?
    '''
    cursor.execute(average_rating_query, (product_id,))

    average_rating = round(cursor.fetchone()[0], 1)

    cursor.execute('''
        UPDATE products 
        SET product_average_rating = ?
        WHERE product_id = ?''', (average_rating, product_id))
    
    conn.commit()
    conn.close()

    return redirect('/electronics/product/' + product_id)