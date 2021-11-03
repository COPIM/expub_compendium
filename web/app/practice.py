# @name: practice.py
# @version: 0.1
# @creation_date: 2021-11-03
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: practice route for practice-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Practice
from werkzeug.exceptions import abort
from . import db

practice = Blueprint('practice', __name__)

# function to retrieve data about a single practice from the database
def get_practice(practice_id):
    practice = Practice.query.filter_by(id=practice_id).first()
    if practice is None:
        abort(404)
    return practice

# route for displaying all practices in database
@practice.route('/practices')
def get_practices():
    practices = Practice.query
    return render_template('practices.html', practices=practices)

# route for displaying a single practice based on the ID in the database
@practice.route('/practices/<int:practice_id>')
def show_practice(practice_id):
    practice = get_practice(practice_id)
    return render_template('practice.html', practice=practice)

# route for editing a single practice based on the ID in the database
@practice.route('/practices/<int:practice_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_practice(practice_id):
    practice = get_practice(practice_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            practice = Practice.query.get(practice_id)
            practice.name = name
            practice.description = description
            db.session.commit()
            return redirect(url_for('practice.get_practices'))

    return render_template('edit.html', practice=practice)

# route for function to delete a single practice from the edit page
@practice.route('/practices/<int:practice_id>/delete', methods=('POST',))
@login_required
def delete_practice(practice_id):
    practice = get_practice(practice_id)
    deletion = Practice.query.get(practice_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')
    return redirect(url_for('practice.get_practices'))
