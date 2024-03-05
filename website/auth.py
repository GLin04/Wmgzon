from flask import Blueprint, abort, render_template, request,redirect, session
import sqlite3

#try blocks are used as tests cannot access the right directory
try:
    from utils import hash_and_salt_password, generate_salt
except ModuleNotFoundError:
    from website.utils import hash_and_salt_password, generate_salt


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']

        # Check if the passwords match
        if password != passwordConfirm:
            return render_template('register.html', error='Passwords do not match')
        
        salt = generate_salt()
        hashed_and_salted_password = hash_and_salt_password(password, salt)

        # Connect to the database
        connection = sqlite3.connect('wmgzon.db')
        cursor = connection.cursor()

        # Insert the data into the database
        cursor.execute("INSERT INTO login_details (user_email, name, hashed_and_salted_password, salt) VALUES (?, ?, ?, ?)",
                       (email, name, hashed_and_salted_password, salt))
        
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
        cursor.execute("SELECT * FROM login_details WHERE user_email=?", (email,))
        user = cursor.fetchone()

        if user is None:
            return render_template('login.html', error='Invalid email or password')
        # Get the user's salt and password
        user_salt = user[4]
        user_password = user[2]

        # Hash and salt the password input
        hashed_and_salted_password = hash_and_salt_password(password, user_salt)

        # If the user exists and the hashed password is correct, log the user in
        if user and user_password == hashed_and_salted_password:
            session['user'] = user
            session['user_email'] = user[0]
            session['user_name'] = user[1]
            session['admin'] = user[3]
            return redirect('/')
        else:
            # If the user doesn't exist, show an error message
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    print(session['user_email'])
    
    # Clear the session data
    session.clear()
    return redirect('/login')


@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()

        # Get the user's input
        old_password_input = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        user_email = session['user_email']

        user_salt = cursor.execute('SELECT salt FROM login_details WHERE user_email=?', (user_email,)).fetchone()[0]

        #salts and hashes the old password input
        hashed_and_salted_old_password_input = hash_and_salt_password(old_password_input, user_salt)


        
        cursor.execute('SELECT hashed_and_salted_password FROM login_details WHERE user_email=?', (user_email,))
        hashed_and_salted_existing_password = cursor.fetchone()[0]

        #checks if the old password is correct and if the new password and confirm password match
        if hashed_and_salted_old_password_input == hashed_and_salted_existing_password and new_password == confirm_password:
            hashed_and_salted_new_password = hash_and_salt_password(new_password, user_salt)
            cursor.execute('UPDATE login_details SET hashed_and_salted_password=? WHERE user_email=?', (hashed_and_salted_new_password, user_email))
            conn.commit()
            conn.close()
            return redirect('/account')
        else:
            conn.close()
            return render_template("change_password.html", error="Invalid password or passwords do not match")

    return render_template("change_password.html")


@auth.route('/give_admin_privileges_page', methods=['GET'])
def give_admin_privileges_page():

    # Check if the user is an admin
    if not session['admin']:
        # If the user is not an admin, show an error message
        abort(403, description="You are not authorised to access this page")

    if request.method == 'GET':
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()

        cursor.execute('SELECT user_email, admin FROM login_details')
        users = cursor.fetchall()
        
        email_list = [user[0] for user in users]

        conn.close()

    # renders the page with the users and their admin status
    return render_template("give_admin_privileges.html", users=users, email_list=email_list)


@auth.route('/give_admin_privileges', methods=['POST'])
def give_admin_privileges():
    if request.method == 'POST':
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()

        user_email = request.form['user_email']
        
        # sets the user to be an admin 
        cursor.execute('UPDATE login_details SET admin=TRUE WHERE user_email=?', (user_email,))
        conn.commit()
        conn.close()

    return redirect('/give_admin_privileges_page')


@auth.route('/remove_admin_privileges', methods=['POST'])
def remove_admin_privileges():
    if request.method == 'POST':
        conn = sqlite3.connect('wmgzon.db')
        cursor = conn.cursor()

        user_email = request.form['user_email']

        # sets the user to not be an admin
        cursor.execute('UPDATE login_details SET admin=FALSE WHERE user_email=?', (user_email,))
        conn.commit()
        conn.close()

    return redirect('/give_admin_privileges_page')