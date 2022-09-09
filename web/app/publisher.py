# @name: publisher.py
# @creation_date: 2022-04-05
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: publisher route for publisher-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .resources import *
from werkzeug.exceptions import abort
from . import db
import os

publisher = Blueprint('publisher', __name__)

# route for displaying all publishers in database
@publisher.route('/publishers/')
def get_publishers():
    publishers = Resource.query.filter_by(type='publisher')
    return render_template('resources.html', resources=publishers, type='publisher')

# route for displaying a single publisher based on the ID in the database
@publisher.route('/publishers/<int:publisher_id>/')
def show_publisher(publisher_id):
    publisher = get_resource(publisher_id)
    links = get_linked_resources(publisher_id)
    return render_template('resource.html', resource=publisher, links=links)

# route for editing a single publisher based on the ID in the database
@publisher.route('/publishers/<int:publisher_id>/edit/', methods=('GET', 'POST'))
@login_required
def edit_publisher(publisher_id):
    publisher = get_resource(publisher_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            publisher = Resource.query.get(publisher_id)
            publisher.name = name
            publisher.description = description
            db.session.commit()
            return redirect(url_for('publisher.get_publishers',_external=True,_scheme=os.environ.get('SSL_SCHEME')))

    return render_template('edit.html', resource=publisher)

# route for function to delete a single publisher from the edit page
@publisher.route('/publishers/<int:publisher_id>/delete/', methods=('POST',))
@login_required
def delete_publisher(publisher_id):
    delete_resource(publisher_id)
    return redirect(url_for('publisher.get_publishers',_external=True,_scheme=os.environ.get('SSL_SCHEME')))
