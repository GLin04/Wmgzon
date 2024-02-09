from flask import render_template, Blueprint

electronics = Blueprint('electronics', __name__)

@electronics.route('/')
def electronics():
    return render_template("electronics.html")