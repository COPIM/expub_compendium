# @name: practice.py
# @creation_date: 2021-11-03
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: practice route for practice-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .resources import *
from .relationships import *
from werkzeug.exceptions import abort
from . import db
import os

practice = Blueprint('practice', __name__)

# route for displaying all practices in database
@practice.route('/practices')
def get_practices():
    practices = Resource.query.filter_by(type='practice')
    return render_template('resources.html', resources=practices, type='practice')

# route for displaying a single practice based on the ID in the database
@practice.route('/practices/<int:practice_id>')
def show_practice(practice_id):
    practice = get_resource(practice_id)
    relationships = get_relationships(practice_id)
    return render_template('resource.html', resource=practice, relationships=relationships)

# route for editing a single practice based on the ID in the database
@practice.route('/practices/<int:practice_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_practice(practice_id):
    practice = get_resource(practice_id)
    resource_dropdown = Resource.query
    existing_relationships = get_relationships(practice_id)

    if request.method == 'POST':
        if not request.form['name']:
            flash('Name is required!')
        else:
            practice = Resource.query.get(practice_id)
            practice.name = request.form['name']
            practice.description = request.form['description']
            practice.experimental = request.form['experimental']
            practice.lessonsLearned = request.form['lessonsLearned']
            practice.references = request.form['references']
            db.session.commit()
            linked_resources = request.form.getlist('linked_resources')
            remove_linked_resources = request.form.getlist('remove_linked_resources')

            edit_relationships(practice_id, linked_resources, remove_linked_resources, existing_relationships)

            return redirect(url_for('practice.get_practices',_external=True,_scheme=os.environ.get('SSL_SCHEME')))

    return render_template('edit.html', resource=practice, resource_dropdown=resource_dropdown, links=existing_relationships)

# route for function to delete a single practice from the edit page
@practice.route('/practices/<int:practice_id>/delete', methods=('POST',))
@login_required
def delete_practice(practice_id):
    delete_resource(practice_id)
    return redirect(url_for('practice.get_practices',_external=True,_scheme=os.environ.get('SSL_SCHEME')))
