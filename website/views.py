from flask import Blueprint, render_template

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


