from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'eszt**?gvujbnokmj!gsd'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import Admin, Post
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(user_id)

    return app

def create_admin():
    from .models import Admin
    app = create_app()  
    with app.app_context():  
        db.create_all()
        if not Admin.query.first():
            admin = Admin(
                email="mrodsut@gmail.com",
                password=generate_password_hash("1234567", method='pbkdf2:sha256')
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')