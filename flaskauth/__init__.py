from flask import Flask
from .main.routes import main
from .extensions import db
from flask_login import LoginManager



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    from . import models
    from .models import Customer
    
    @login_manager.user_loader
    def load_customer(id):
        return Customer.query.get(int(id))

    with app.app_context():
        db.create_all()
    app.register_blueprint(main)

    
    return app
