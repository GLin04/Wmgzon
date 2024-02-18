from flask import Blueprint, render_template
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

    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    # close the connection
    conn.close()

    # render the template with the product details
    return render_template("product.html", product=product)