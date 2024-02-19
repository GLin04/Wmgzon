from flask import Blueprint, render_template, request,redirect, session
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

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Connect to the database
        connection = sqlite3.connect('wmgzon.db')
        cursor = connection.cursor()

        # Check if the email and password match a user in the database
        cursor.execute("SELECT * FROM login_details WHERE email=?", (email,))
        user = cursor.fetchone()

        if user and user[2] == password:
            session['user'] = user
            session['user_email'] = user[0]
            session['user_name'] = user[1]
            return redirect('/')
        else:
            # If the user doesn't exist, show an error message
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_email', None)
    session.pop('user_name', None)
    return redirect('/login')
