from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/register')
def login():
    return render_template("register.html")
