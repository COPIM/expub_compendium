# @name: reference.py
# @creation_date: 2022-02-08
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: reference route for reference-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from werkzeug.exceptions import abort
from . import db

reference = Blueprint('reference', __name__)

# function to retrieve data about a single reference from the database
def get_reference(reference_id):
    reference = Reference.query.filter_by(id=reference_id).first()
    if reference is None:
        abort(404)
    return reference

# route for displaying all references in database
@reference.route('/references')
def get_references():
    references = Reference.query
    return render_template('references.html', references=references)

# route for displaying a single reference based on the ID in the database
@reference.route('/references/<int:reference_id>')
def show_reference(reference_id):
    reference = get_reference(reference_id)
    return render_template('reference.html', reference=reference)

# route for editing a single reference based on the ID in the database
@reference.route('/references/<int:reference_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_reference(reference_id):
    reference = get_reference(reference_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            reference = Reference.query.get(reference_id)
            reference.name = name
            reference.description = description
            db.session.commit()
            return redirect(url_for('reference.get_references'))

    return render_template('edit.html', reference=reference)

# route for function to delete a single reference from the edit page
@reference.route('/references/<int:reference_id>/delete', methods=('POST',))
@login_required
def delete_reference(reference_id):
    reference = get_reference(reference_id)
    deletion = Reference.query.get(reference_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')
    return redirect(url_for('reference.get_references'))
