from flask import Blueprint, render_template, request,redirect, url_for
import sqlite3

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        # Connect to the database
        connection = sqlite3.connect('wmgzon.db')
        cursor = connection.cursor()

        # Insert the data into the database
        cursor.execute("INSERT INTO login_details (email, name, password) VALUES (?, ?, ?)",
                       (email, name, password))
        
        # Commit changes and close the connection
        connection.commit()
        return redirect('/login')
    return render_template("register.html")

@auth.route('/login')
def login():

    return render_template("login.html")

