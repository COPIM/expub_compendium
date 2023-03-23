# @name: main.py
# @creation_date: 2021-10-20
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Main route for index and other pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Resource
from sqlalchemy.sql import func
import markdown

main = Blueprint('main', __name__)

# route for index page
@main.route('/')
def index():
    tools = Resource.query.filter_by(type='tool').order_by(func.random()).limit(1).all()
    books = Resource.query.filter_by(type='book').order_by(func.random()).limit(1).all()
    tools2 = Resource.query.filter_by(type='tool').order_by(func.random()).limit(1).all()
    books2 = Resource.query.filter_by(type='book').order_by(func.random()).limit(1).all()
    with open('content/home.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('index.html', text=text, tools=tools,books=books, tools2=tools2,books2=books2)

# route for profile page
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

# route for test page
@main.route('/test')
def test():
    return render_template('test.html')

# route for about page
@main.route('/about')
def about():
    with open('content/about.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('about.html', text=text)
