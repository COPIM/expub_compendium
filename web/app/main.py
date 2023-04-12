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
from .resources import *
from .relationships import *
from sqlalchemy.sql import func
import markdown

main = Blueprint('main', __name__)

# route for index page
@main.route('/')
def index():
    view = request.args.get('view')
    # curated list of resources to display on homepage
    tool_ids = ['4','10', '34', '27']
    practice_ids = ['53', '59', '65', '56']
    book_ids = ['94', '72', '105', '67']
    # concatenate lists of resources
    resource_ids = tool_ids + practice_ids + book_ids
    # get data for curated resources
    curated = get_curated_resources(resource_ids)
    with open('content/home.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('index.html', text=text, resources=curated, view=view)

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
        about_text = f.read()
        about_text = markdown.markdown(about_text)
    with open('content/colophon.md', 'r') as f:
        colophon_text = f.read()
        colophon_text = markdown.markdown(colophon_text)
    return render_template('about.html', about_text=about_text, colophon_text=colophon_text)
