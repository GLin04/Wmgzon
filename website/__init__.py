from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secrets'
    
    from .views import views
    from .auth import auth
    from .electronics import electronics

    app.register_blueprint(electronics, url_prefix='/electronics')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app