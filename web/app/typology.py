# @name: typology.py
# @creation_date: 2022-04-05
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: typology route for typology-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .resources import *
from werkzeug.exceptions import abort
from . import db

typology = Blueprint('typology', __name__)

# route for displaying all typologies in database
@typology.route('/typologies')
def get_typologies():
    typologies = Resource.query.filter_by(type='typology')
    return render_template('resources.html', resources=typologies, type='typology')

# route for displaying a single typology based on the ID in the database
@typology.route('/typologies/<int:typology_id>')
def show_typology(typology_id):
    typology = get_resource(typology_id)
    links = get_linked_resources(typology_id)
    return render_template('resource.html', resource=typology, links=links)

# route for editing a single typology based on the ID in the database
@typology.route('/typologies/<int:typology_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_typology(typology_id):
    typology = get_resource(typology_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            typology = Resource.query.get(typology_id)
            typology.name = name
            typology.description = description
            db.session.commit()
            return redirect(url_for('typology.get_typologies'))

    return render_template('edit.html', resource=typology)

# route for function to delete a single typology from the edit page
@typology.route('/typologies/<int:typology_id>/delete', methods=('POST',))
@login_required
def delete_typology(typology_id):
    delete_resource(typology_id)
    return redirect(url_for('typology.get_typologies'))
