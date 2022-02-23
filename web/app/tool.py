# @name: tool.py
# @version: 0.1
# @creation_date: 2021-10-20
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: tool route for tool-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .models import Relationships
from werkzeug.exceptions import abort
from . import db

tool = Blueprint('tool', __name__)

# function to retrieve data about a single tool from the database
def get_tool(tool_id):
    tool = Resource.query.filter_by(id=tool_id).first()
    if tool is None:
        abort(404)
    return tool

# function to retrieve linked resources
def get_linked_resources(tool_id):
    relationships = Relationships.query.filter_by(first_resource_id=tool_id).first()
    if relationships:
        resource_id = relationships.second_resource_id
        resources = Resource.query.filter_by(id=resource_id).all()
        return resources

# route for displaying all tools in database
@tool.route('/tools')
def get_tools():
    tools = Resource.query.filter_by(type='tool')
    return render_template('tools.html', tools=tools)

# route for displaying a single tool based on the ID in the database
@tool.route('/tools/<int:tool_id>')
def show_tool(tool_id):
    tool = get_tool(tool_id)
    resources = get_linked_resources(tool_id)
    return render_template('tool.html', tool=tool, resources=resources)

# route for editing a single tool based on the ID in the database
@tool.route('/tools/<int:tool_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_tool(tool_id):
    tool = get_tool(tool_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            tool = Resource.query.get(tool_id)
            tool.name = name
            tool.description = description
            tool.projectUrl = project_url
            tool.repositoryUrl = repository_url
            tool.dependencies = dependencies
            tool.expertiseToUse = expertise
            tool.expertiseToHost = self_host_expertise
            tool.ingestFormats = ingest
            tool.outputFormats = output
            tool.status = status
            db.session.commit()
            return redirect(url_for('tool.get_tools'))

    return render_template('edit.html', resource=tool)

# route for function to delete a single tool from the edit page
@tool.route('/tools/<int:tool_id>/delete', methods=('POST',))
@login_required
def delete_tool(tool_id):
    tool = get_tool(tool_id)
    deletion = Resource.query.get(tool_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')
    return redirect(url_for('tool.get_tools'))
