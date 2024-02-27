from flask import Blueprint, render_template, request, session
import sqlite3
electronics = Blueprint('electronics', __name__)

@electronics.route('/')
def products():


    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    # close the connection
    conn.close()

    # render the template with the products list
    return render_template("electronics.html", products=products)

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
    return render_template("product.html", product=product, product_ids=product_ids)



@electronics.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['search_input']

        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM products
            WHERE name LIKE ?
        ''', ('%' + keyword + '%',))

        results = cursor.fetchall()
        conn.close()

        # Pass the results to the search_results template
        return render_template('search_results.html', results=results, search_term=keyword)