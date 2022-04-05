# @name: workflow.py
# @creation_date: 2022-04-05
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: workflow route for workflow-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .resources import *
from werkzeug.exceptions import abort
from . import db

workflow = Blueprint('workflow', __name__)

# route for displaying all workflows in database
@workflow.route('/workflows')
def get_workflows():
    workflows = Resource.query.filter_by(type='workflow')
    return render_template('resources.html', resources=workflows, type='workflow')

# route for displaying a single workflow based on the ID in the database
@workflow.route('/workflows/<int:workflow_id>')
def show_workflow(workflow_id):
    workflow = get_resource(workflow_id)
    links = get_linked_resources(workflow_id)
    return render_template('resource.html', resource=workflow, links=links)

# route for editing a single workflow based on the ID in the database
@workflow.route('/workflows/<int:workflow_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_workflow(workflow_id):
    workflow = get_resource(workflow_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            workflow = Resource.query.get(workflow_id)
            workflow.name = name
            workflow.description = description
            db.session.commit()
            return redirect(url_for('workflow.get_workflows'))

    return render_template('edit.html', resource=workflow)

# route for function to delete a single workflow from the edit page
@workflow.route('/workflows/<int:workflow_id>/delete', methods=('POST',))
@login_required
def delete_workflow(workflow_id):
    delete_resource(workflow_id)
    return redirect(url_for('workflow.get_workflows'))
