# @name: __init__.py
# @creation_date: 2021-10-20
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Initialises the app, SQLAlchemy, and configuration variables
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
# Config stuff adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
import os

# initiate SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# initiate Moment for datetime functions
moment = Moment()

def create_app():
    app = Flask(__name__)

    # get config variables from OS environment variables: set in env file passed through Docker Compose
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    moment.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for main parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for tools parts of app
    from .tool import tool as tool_blueprint
    app.register_blueprint(tool_blueprint)

    # blueprint for practice parts of app
    from .practice import practice as practice_blueprint
    app.register_blueprint(practice_blueprint)

    # blueprint for publisher parts of app
    from .publisher import publisher as publisher_blueprint
    app.register_blueprint(publisher_blueprint)

    # blueprint for book parts of app
    from .book import book as book_blueprint
    app.register_blueprint(book_blueprint)

    # blueprint for create parts of app
    from .create import create as create_blueprint
    app.register_blueprint(create_blueprint)

    return app
