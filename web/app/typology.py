# @name: typology.py
# @version: 0.1
# @creation_date: 2022-02-08
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: typology route for typology-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from werkzeug.exceptions import abort
from . import db

typology = Blueprint('typology', __name__)

# function to retrieve data about a single typology from the database
def get_typology(typology_id):
    typology = Typology.query.filter_by(id=typology_id).first()
    if typology is None:
        abort(404)
    return typology

# route for displaying all typologies in database
@typology.route('/typologies')
def get_typologies():
    typologies = Typology.query
    return render_template('typologies.html', typologies=typologies)

# route for displaying a single typology based on the ID in the database
@typology.route('/typologies/<int:typology_id>')
def show_typology(typology_id):
    typology = get_typology(typology_id)
    return render_template('typology.html', typology=typology)

# route for editing a single typology based on the ID in the database
@typology.route('/typologies/<int:typology_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_typology(typology_id):
    typology = get_typology(typology_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            typology = Typology.query.get(typology_id)
            typology.name = name
            typology.description = description
            db.session.commit()
            return redirect(url_for('typology.get_typologies'))

    return render_template('edit.html', typology=typology)

# route for function to delete a single typology from the edit page
@typology.route('/typologies/<int:typology_id>/delete', methods=('POST',))
@login_required
def delete_typology(typology_id):
    typology = get_typology(typology_id)
    deletion = Typology.query.get(typology_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')
    return redirect(url_for('typology.get_typologies'))
