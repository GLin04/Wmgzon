from flask import Flask

#try blocks are used as tests cannot access the right directory
try:
    from electronics import electronics
except ModuleNotFoundError:
    from website.electronics import electronics

try:
    from views import views
except ModuleNotFoundError:
    from website.views import views

try:
    from website.auth import auth
    
except ModuleNotFoundError:
    from auth import auth




def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secrets'
    
    # Register the blueprints
    app.register_blueprint(electronics, url_prefix='/electronics')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
