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
from werkzeug.exceptions import abort
from . import db

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
    links = get_linked_resources(practice_id)
    return render_template('resource.html', resource=practice, links=links)

# route for editing a single practice based on the ID in the database
@practice.route('/practices/<int:practice_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_practice(practice_id):
    practice = get_resource(practice_id)
    resource_dropdown = Resource.query
    links = get_linked_resources(practice_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        linked_resources = request.form.getlist('linked_resources')
        remove_linked_resources = request.form.getlist('remove_linked_resources')

        if not name:
            flash('Name is required!')
        else:
            practice = Resource.query.get(practice_id)
            practice.name = name
            practice.description = description
            db.session.commit()
            if linked_resources:
                for linked_resource in linked_resources:
                    link = Resource.query.get(linked_resource)
                    if links and link not in links:
                        add_linked_resource(practice_id, linked_resource)
                    elif not links:
                        add_linked_resource(practice_id, linked_resource)
            if remove_linked_resources:
                for remove_linked_resource in remove_linked_resources:
                    delete_relationship(practice_id, remove_linked_resource)
            return redirect(url_for('practice.get_practices'))

    return render_template('edit.html', resource=practice, resource_dropdown=resource_dropdown, links=links)

# route for function to delete a single practice from the edit page
@practice.route('/practices/<int:practice_id>/delete', methods=('POST',))
@login_required
def delete_practice(practice_id):
    delete_resource(practice_id)
    return redirect(url_for('practice.get_practices'))
