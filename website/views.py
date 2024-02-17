from flask import Blueprint, render_template, request

import sqlite3

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/login')
def login():
    return render_template("login.html")

@views.route('/register')
def register():
    return render_template("register.html")

@views.route('/coming_soon')
def coming_soon():
    return render_template("coming_soon.html")

@views.route('/basket')
def basket():
    return render_template("basket.html")

@views.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method=='POST':

        # Get the data from the HTML form
        name = str(request.form['name'])
        stock = int(request.form['stock'])
        product_type = str(request.form['productType'])
        price = float(request.form['price'])
        delivery_time = int(request.form['deliveryTime'])
        brand = str(request.form['brand'])
        specifications = str(request.form['specifications'])
        description = str(request.form['description'])

        # Connect to the database
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()

        # Insert the data into the database
        cursor.execute('''
            INSERT INTO products (name, stock, productType, price, deliveryTime, brand, specifications, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, stock, product_type, price, delivery_time, brand, specifications, description))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

    return render_template("add_product.html")

