from flask import Blueprint, render_template

electronics = Blueprint('electronics', __name__)

@electronics.route('/')
def products():
    return render_template("electronics.html")