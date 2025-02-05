# @name: tool.py
# @creation_date: 2021-10-20
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: tool route for tool-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .resources import *
from .relationships import *
from . import db
import os
from sqlalchemy.sql import func
import markdown

tool = Blueprint('tool', __name__)

# route for displaying all tools in database
@tool.route('/tools')
def get_tools():
    # GET PARAMETERS
    # get URL parameters for views and pages
    view = request.args.get('view')
    page = request.args.get('page', 1, type=int)
    # set resource type
    resource_type = 'tool'
    # get introductory paragraph Markdown
    with open('content/tools.md', 'r') as f:
        intro_text = f.read()
        intro_text = markdown.markdown(intro_text)

    # DATABASE QUERY
    tools_query = Resource.query.filter_by(type=resource_type).filter_by(published=True)

    # FILTERING
    for key in request.args.keys():
        if key != 'view' and key != 'page':
            if (key == 'practice' and request.args.get(key) != ''):
                tools_1 = tools_query.join(Relationship, Relationship.first_resource_id == Resource.id, isouter=True).filter(Relationship.second_resource_id==request.args.get(key))
                tools_2 = tools_query.join(Relationship, Relationship.second_resource_id == Resource.id, isouter=True).filter(Relationship.first_resource_id==request.args.get(key))
                tools_query = tools_1.union(tools_2)
            if (key == 'scriptingLanguage' and request.args.get(key) != ''):
                regex = request.args.get(key) + "$|" + request.args.get(key) + "\s\/"
                tools_query = tools_query.filter(Resource.scriptingLanguage.regexp_match(regex))
            if ((key != 'practice' and key != 'scriptingLanguage') and request.args.get(key) != ''):
                kwargs = {key: request.args.get(key)}
                tools_query = tools_query.filter_by(**kwargs)

    # finalise the query and add pagination
    tools = tools_query.order_by(Resource.name).paginate(page=page, per_page=25)

    # FILTERS MENU
    # get values for filter menu dropdowns
    # practices 
    practices_filter = Resource.query.filter_by(type='practice').filter_by(published=True).with_entities(Resource.id, Resource.name).all()
    # license
    licenses_filter = get_filter_values('license', resource_type)
    # language
    languages_filter = get_filter_values('scriptingLanguage', resource_type)
    # status
    status_filter = get_filter_values('status', resource_type)
 
    # POST-FILTERING PROCESSING
    # if view is 'expanded' then append relationships
    if view != 'list':
        # append relationships to each book
        append_relationships_multiple_paginated(tools)

    return render_template('resources.html', resources=tools, type=resource_type, practices_filter=practices_filter, licenses_filter=licenses_filter, languages_filter=languages_filter, status_filter=status_filter, view=view, page=page, intro_text=intro_text)

# route for displaying a single tool based on the ID in the database
@tool.route('/tools/<int:tool_id>')
def show_tool(tool_id):
    tool = get_full_resource(tool_id)
    return render_template('resource.html', resource=tool)

# route for editing a single tool based on the ID in the database
@tool.route('/tools/<int:tool_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_tool(tool_id):
    tool = get_resource(tool_id)
    resource_dropdown = Resource.query.order_by(Resource.name)
    existing_relationships = get_relationships(tool_id)

    if request.method == 'POST':
        if not request.form['name']:
            flash('Name is required!')
        else:
            tool = Resource.query.get(tool_id)
            tool.name = request.form['name']
            tool.description = request.form['description']
            tool.developer = request.form['developer']
            tool.developerUrl = request.form['developerUrl']
            tool.projectUrl = request.form['projectUrl']
            tool.repositoryUrl = request.form['repositoryUrl']
            tool.license = request.form['license']
            tool.scriptingLanguage = request.form['scriptingLanguage']
            tool.expertiseToUse = request.form['expertiseToUse']
            tool.expertiseToHost = request.form['expertiseToHost']
            tool.dependencies = request.form['dependencies']
            tool.ingestFormats = request.form['ingestFormats']
            tool.outputFormats = request.form['outputFormats']
            tool.status = request.form['status']
            tool.videoUrl = request.form['videoUrl']
            db.session.commit()
            linked_resources = request.form.getlist('linked_practices') + request.form.getlist('linked_books')
            remove_linked_resources = request.form.getlist('remove_linked_resources')

            edit_relationships(tool_id, linked_resources, remove_linked_resources, existing_relationships)
            
            return redirect(url_for('tool.get_tools',_external=True,_scheme=os.environ.get('SSL_SCHEME')))

    return render_template('edit.html', resource=tool, resource_dropdown=resource_dropdown, relationships=existing_relationships)

# route for function to delete a single tool from the edit page
@tool.route('/tools/<int:tool_id>/delete', methods=('POST',))
@login_required
def delete_tool(tool_id):
    delete_resource(tool_id)
    return redirect(url_for('tool.get_tools',_external=True,_scheme=os.environ.get('SSL_SCHEME')))
