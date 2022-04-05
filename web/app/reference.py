# @name: reference.py
# @creation_date: 2022-04-05
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: reference route for reference-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .resources import *
from werkzeug.exceptions import abort
from . import db

reference = Blueprint('reference', __name__)

# route for displaying all references in database
@reference.route('/references')
def get_references():
    references = Resource.query.filter_by(type='reference')
    return render_template('resources.html', resources=references, type='reference')

# route for displaying a single reference based on the ID in the database
@reference.route('/references/<int:reference_id>')
def show_reference(reference_id):
    reference = get_resource(reference_id)
    links = get_linked_resources(reference_id)
    return render_template('resource.html', resource=reference, links=links)

# route for editing a single reference based on the ID in the database
@reference.route('/references/<int:reference_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_reference(reference_id):
    reference = get_resource(reference_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            reference = Resource.query.get(reference_id)
            reference.name = name
            reference.description = description
            db.session.commit()
            return redirect(url_for('reference.get_references'))

    return render_template('edit.html', resource=reference)

# route for function to delete a single reference from the edit page
@reference.route('/references/<int:reference_id>/delete', methods=('POST',))
@login_required
def delete_reference(reference_id):
    delete_resource(reference_id)
    return redirect(url_for('reference.get_references'))
