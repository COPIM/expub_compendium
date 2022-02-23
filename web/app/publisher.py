# @name: publisher.py
# @version: 0.1
# @creation_date: 2022-02-08
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: publisher route for publisher-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from werkzeug.exceptions import abort
from . import db

publisher = Blueprint('publisher', __name__)

# function to retrieve data about a single publisher from the database
def get_publisher(publisher_id):
    publisher = Publisher.query.filter_by(id=publisher_id).first()
    if publisher is None:
        abort(404)
    return publisher

# route for displaying all publishers in database
@publisher.route('/publishers')
def get_publishers():
    publishers = Publisher.query
    return render_template('publishers.html', publishers=publishers)

# route for displaying a single publisher based on the ID in the database
@publisher.route('/publishers/<int:publisher_id>')
def show_publisher(publisher_id):
    publisher = get_publisher(publisher_id)
    return render_template('publisher.html', publisher=publisher)

# route for editing a single publisher based on the ID in the database
@publisher.route('/publishers/<int:publisher_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_publisher(publisher_id):
    publisher = get_publisher(publisher_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            publisher = Publisher.query.get(publisher_id)
            publisher.name = name
            publisher.description = description
            db.session.commit()
            return redirect(url_for('publisher.get_publishers'))

    return render_template('edit.html', publisher=publisher)

# route for function to delete a single publisher from the edit page
@publisher.route('/publishers/<int:publisher_id>/delete', methods=('POST',))
@login_required
def delete_publisher(publisher_id):
    publisher = get_publisher(publisher_id)
    deletion = Publisher.query.get(publisher_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')
    return redirect(url_for('publisher.get_publishers'))
