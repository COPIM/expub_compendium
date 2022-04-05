# @name: sensitivity.py
# @creation_date: 2022-02-08
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: sensitivity route for sensitivity-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .resources import *
from werkzeug.exceptions import abort
from . import db

sensitivity = Blueprint('sensitivity', __name__)

# route for displaying all sensitivities in database
@sensitivity.route('/sensitivities')
def get_sensitivities():
    sensitivities = Resource.query.filter_by(type='sensitivity')
    return render_template('resources.html', resources=sensitivities, type='sensitivity')

# route for displaying a single sensitivity based on the ID in the database
@sensitivity.route('/sensitivities/<int:sensitivity_id>')
def show_sensitivity(sensitivity_id):
    sensitivity = get_resource(sensitivity_id)
    links = get_linked_resources(sensitivity_id)
    return render_template('resource.html', resource=sensitivity, links=links)

# route for editing a single sensitivity based on the ID in the database
@sensitivity.route('/sensitivities/<int:sensitivity_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_sensitivity(sensitivity_id):
    sensitivity = get_resource(sensitivity_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            sensitivity = Resource.query.get(sensitivity_id)
            sensitivity.name = name
            sensitivity.description = description
            db.session.commit()
            return redirect(url_for('sensitivity.get_sensitivities'))

    return render_template('edit.html', sensitivity=sensitivity)

# route for function to delete a single sensitivity from the edit page
@sensitivity.route('/sensitivities/<int:sensitivity_id>/delete', methods=('POST',))
@login_required
def delete_sensitivity(sensitivity_id):
    delete_resource(sensitivity_id)
    return redirect(url_for('sensitivity.get_sensitivities'))
