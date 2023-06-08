from flask import Flask, session, app
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
from flask_talisman import Talisman
import uuid

ckeditor = CKEditor()
csrf = CSRFProtect()

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = str(uuid.uuid4().hex)
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}.sqlite'
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['ALLOWED_HOSTS'] = ["litenotes.herokuapp.com"]
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
    
    db.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)

    csp = {
    'default-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'cdnjs.cloudflare.com',
            'cdn.jsdelivr.net',
            'code.jquery.com',
            'maxcdn.bootstrapcdn.com',
            'fontawesome.com',
            'fonts.googleapis.com',
            'cdn.ckeditor.com',
            'w3.org',
        ],
        'img-src': [
            '*',
            'data:',
        ]
    }

    talisman = Talisman(app, content_security_policy=csp)

    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')



if __name__ == '__main__':
    app = create_app()
    # app.run(debug=True, host= '192.168.1.140', port=5000)
    app.run(debug=True)
else:
    gunicorn_app = create_app()

