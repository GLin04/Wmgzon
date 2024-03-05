import os
import shutil
import sqlite3
import pytest
import tempfile

from website.views import views
from website.auth import auth
from website.electronics import electronics
from website.__init__ import create_app


@pytest.fixture(autouse=True)
def setup_before_each_test():
    
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = '1'")


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True


    with app.test_client() as client:
        yield client


#test if the home route redirects to the electronics route
def test_home_route_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/electronics'


#test if the account route is accessible
def test_account_route(client):
    response = client.get('/account')
    assert response.status_code == 200
    assert b'<span style="font-size:1.5rem">Account Options</span>' in response.data

#test if the coming_soon route is accessible
def test_coming_soon_route(client):
    response = client.get('/coming_soon')
    assert response.status_code == 200
    assert b'<h1 class="coming-soon-text">Page coming soon!</h1>' in response.data

#test if the basket route is accessible with session data
def test_basket_route(client):
    with client.session_transaction() as sess:
        sess['user_email'] = 'test@example.com'
        sess['postcode'] = ['12345','']

    response = client.get('/basket')
    assert response.status_code == 200
    assert b'<div class="basket-main-container">' in response.data


#test if the product route is accessible
def test_add_product_route(client):
    with client.session_transaction() as sess:
        sess['admin'] = True


    response = client.get('/add_product')
    assert response.status_code == 200
    assert b'<div class="add-product-main-container main-container">' in response.data


#test if the add product post request functions with test data
def test_add_product_route_post(client):
    with client.session_transaction() as sess:
        sess['admin'] = True

    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    temp_file.write(b'some_image_data')
    temp_file.seek(0)


    # Test POST request
    data = {
        'name': 'Test Product',
        'stock': 10,
        'productType': 'accessories',
        'price': 99.99,
        'deliveryTime': 3,
        'brand': 'Test Brand',
        'specifications': 'Test Specifications',
        'description': 'Test Description',
        'inputFile': (temp_file, 'test_image.jpg')
    }
    response = client.post('/add_product', data=data)

    assert response.status_code == 302
    assert response.headers['Location'] == '/electronics'

    # Delete the inserted data from the database
    temp_file.close()
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE name = 'Test Product'")
    conn.commit()
    conn.close()



#test if the edit product route is accessible
def test_edit_product_route(client):
    with client.session_transaction() as sess:
        sess['admin'] = True

    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT product_id FROM products")
    product_id = cursor.fetchone()[0]
    print(product_id)

    # Test GET request if there is a product in the database
    if product_id is None:
        print("No products in the database")
    else:
        response = client.get(f'/edit_product/{product_id}')
        assert response.status_code == 200
        assert b'<div class="add-product-main-container main-container">' in response.data
    conn.close()


#test if the edit product post request functions with test data
def test_edit_product_route_post(client):
    with client.session_transaction() as sess:
        sess['admin'] = True
        
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    temp_file.write(b'some_image_data')
    temp_file.seek(0)

    # Insert a product into the database to edit
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (product_id, name, stock, productType, price, deliveryTime, brand, specifications, description, product_image) VALUES ( '1', 'Test Product', 10, 'accessories', 99.99, 3, 'Test Brand', 'Test Specifications', 'Test Description', 'test_image.jpg')")
    conn.commit()

    existing_product_id = 1

    # Test POST request to edit the existing product with ID 1
    data = {
        'name': 'Edited Test Product',
        'stock': 15,
        'productType': 'tvs',
        'price': 129.99,
        'deliveryTime': 5,
        'brand': 'Edited Test Brand',
        'specifications': 'Edited Test Specifications',
        'description': 'Edited Test Description',
        'inputFile': (temp_file, 'test_image.jpg')
    }
    response = client.post(f'/edit_product/{existing_product_id}', data=data)


    assert response.status_code == 302  
    assert response.headers['Location'] == '/electronics'

    # Delete the inserted data from the database
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = '1'")
    conn.commit()
    conn.close()



#test if the delete product route deletes a product from the database
def test_delete_product_route(client):
    with client.session_transaction() as sess:
        sess['admin'] = True


    # Insert a product into the database to delete
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (product_id, name, stock, productType, price, deliveryTime, brand, specifications, description) VALUES ( '1', 'Test Product', 10, 'accessories', 99.99, 3, 'Test Brand', 'Test Specifications', 'Test Description')")
    conn.commit()


    response = client.delete('/delete_product/1')
    assert response.status_code == 302
    assert response.headers['Location'] == '/electronics'


#test if the add to basket post request functions with test data
def test_add_to_basket_route(client):
    with client.session_transaction() as sess:
        sess['user_email'] = 'test@example.com'

    # Insert a product into the database to add to the basket
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (product_id, name, stock, productType, price, deliveryTime, brand, specifications, description) VALUES ( '1', 'Test Product', 10, 'accessories', 99.99, 3, 'Test Brand', 'Test Specifications', 'Test Description')")
    conn.commit()

    data = {
        'product_id': 1,
        'quantity': 2,
        'prof_installation_hidden': False,
        'total_hidden': 199.98
    }

    # Test if post request is processed correctly
    response = client.post('/add_to_basket', data=data)
    assert response.status_code == 302
    assert response.headers['Location'] == '/basket'

    # Delete the inserted data from the database
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM basket WHERE user_email = 'test@example.com'")
    conn.commit()

    # Delete the inserted data from the database
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = '1'")
    conn.commit()

    conn.close()



def test_update_basket_route(client):
    with client.session_transaction() as sess:
        sess['user_email'] = 'test@example.com'

    # Insert a product into the database to add to the basket
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (product_id, name, stock, productType, price, deliveryTime, brand, specifications, description) VALUES ( '1', 'Test Product', 10, 'accessories', 99.99, 3, 'Test Brand', 'Test Specifications', 'Test Description')")
    conn.commit()
    cursor.execute("INSERT INTO basket (user_email, product_id, product_quantity, total_price) VALUES (?, ?, ?, ?)",
               (sess['user_email'], 1, 1, 99.99))
    conn.commit()

    # Inputs data to update the basket
    data = {
        'productId': 1,
        'quantity': 3,
        'total': 299.97
    }
    response = client.put('/update_basket', query_string=data)

    cursor.execute("SELECT * FROM basket WHERE user_email = ?", (sess['user_email'],))
    updated_quantity = cursor.fetchone()[2]

    # Checks if the product quantity was updated to 3
    assert updated_quantity == 3
    assert response.status_code == 302
    assert response.headers['Location'] == '/basket'

    # Delete the inserted data from the database
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM basket WHERE user_email = ?", (sess['user_email'],))
    conn.commit()
    cursor.execute("DELETE FROM products WHERE product_id = '1'")
    conn.commit()
    conn.close()


# Check if the delete request is processed correctly
def test_delete_from_basket_delete(client):
    with client.session_transaction() as sess:
        sess['user_email'] = 'test@example.com'

    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()

    # Add the product to the basket
    cursor.execute("INSERT INTO basket (user_email, product_id, product_quantity, total_price) VALUES (?, ?, ?, ?)",
                (sess['user_email'], 1, 1, 99.99))
    conn.commit()

    # Test if delete request is processed correctly
    data = {
        'productId': 1
    }
    response = client.delete('/delete_basket', query_string=data)

    cursor.execute("SELECT * FROM basket WHERE user_email = ?", (sess['user_email'],))
    basket_product = cursor.fetchone()

    # Checks if the product was deleted from the basket
    assert basket_product is None
    assert response.status_code == 302
    assert response.headers['Location'] == '/basket'
    conn.close()



def test_checkout_route(client):
    with client.session_transaction() as sess:
        sess['user_email'] = 'test@example.com'
        sess['postcode'] = ['12345']

    response = client.get('/checkout')
    assert response.status_code == 200
    assert b'checkout.html' in response.data
