# @name: sensitivity.py
# @version: 0.1
# @creation_date: 2022-02-08
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: sensitivity route for sensitivity-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Sensitivity
from werkzeug.exceptions import abort
from . import db

sensitivity = Blueprint('sensitivity', __name__)

# function to retrieve data about a single sensitivity from the database
def get_sensitivity(sensitivity_id):
    sensitivity = Sensitivity.query.filter_by(id=sensitivity_id).first()
    if sensitivity is None:
        abort(404)
    return sensitivity

# route for displaying all sensitivities in database
@sensitivity.route('/sensitivities')
def get_sensitivities():
    sensitivities = Sensitivity.query
    return render_template('sensitivities.html', sensitivities=sensitivities)

# route for displaying a single sensitivity based on the ID in the database
@sensitivity.route('/sensitivities/<int:sensitivity_id>')
def show_sensitivity(sensitivity_id):
    sensitivity = get_sensitivity(sensitivity_id)
    return render_template('sensitivity.html', sensitivity=sensitivity)

# route for editing a single sensitivity based on the ID in the database
@sensitivity.route('/sensitivities/<int:sensitivity_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_sensitivity(sensitivity_id):
    sensitivity = get_sensitivity(sensitivity_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            sensitivity = Sensitivity.query.get(sensitivity_id)
            sensitivity.name = name
            sensitivity.description = description
            db.session.commit()
            return redirect(url_for('sensitivity.get_sensitivities'))

    return render_template('edit.html', sensitivity=sensitivity)

# route for function to delete a single sensitivity from the edit page
@sensitivity.route('/sensitivities/<int:sensitivity_id>/delete', methods=('POST',))
@login_required
def delete_sensitivity(sensitivity_id):
    sensitivity = get_sensitivity(sensitivity_id)
    deletion = Sensitivity.query.get(sensitivity_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')
    return redirect(url_for('sensitivity.get_sensitivities'))
