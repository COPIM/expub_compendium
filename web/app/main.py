# @name: main.py
# @version: 0.1
# @creation_date: 2021-10-20
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Main route for index and other pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from .models import Tool
from sqlalchemy.sql import func

main = Blueprint('main', __name__)

# route for index page
@main.route('/')
def index():
    tools = Tool.query.order_by(func.random()).limit(5).all()
    return render_template('index.html', tools=tools)

# route for profile page
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

# route for test page
@main.route('/test')
def test():
    return render_template('test.html')
