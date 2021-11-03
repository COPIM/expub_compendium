# @name: example.py
# @version: 0.1
# @creation_date: 2021-11-03
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: example route for example-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Example
from werkzeug.exceptions import abort
from . import db

example = Blueprint('example', __name__)

# function to retrieve data about a single example from the database
def get_example(example_id):
    example = Example.query.filter_by(id=example_id).first()
    if example is None:
        abort(404)
    return example

# route for displaying all examples in database
@example.route('/examples')
def get_examples():
    examples = Example.query
    return render_template('examples.html', examples=examples)

# route for displaying a single example based on the ID in the database
@example.route('/examples/<int:example_id>')
def show_example(example_id):
    example = get_example(example_id)
    return render_template('example.html', example=example)

# route for editing a single example based on the ID in the database
@example.route('/examples/<int:example_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_example(example_id):
    example = get_example(example_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            example = Example.query.get(example_id)
            example.name = name
            example.description = description
            db.session.commit()
            return redirect(url_for('example.get_examples'))

    return render_template('edit.html', example=example)

# route for function to delete a single example from the edit page
@example.route('/examples/<int:example_id>/delete', methods=('POST',))
@login_required
def delete_example(example_id):
    example = get_example(example_id)
    deletion = Example.query.get(example_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')
    return redirect(url_for('example.get_examples'))
