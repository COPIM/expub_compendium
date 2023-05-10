# @name: practice.py
# @creation_date: 2021-11-03
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: practice route for practice-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .resources import *
from .relationships import *
from . import db
import os
import markdown
from sqlalchemy.sql import func
from sqlalchemy import or_

practice = Blueprint('practice', __name__)

# route for displaying all practices in database
@practice.route('/practices')
def get_practices():
    # get introductory paragraph Markdown
    with open('content/practices.md', 'r') as f:
        intro_text = f.read()
        intro_text = markdown.markdown(intro_text)
    view = request.args.get('view')
    practices = Resource.query.filter_by(type='practice').order_by(func.random())
    # temporarily removing incomplete practices from main list
    practices = Resource.query.filter(
        or_(
            Resource.id==53,
            Resource.id==56,
            Resource.id==59,
            Resource.id==62,
            Resource.id==63,
            Resource.id==65,
            Resource.id==66
        ))
    # finalise the query
    practices = practices.all()
    # get number of practices
    count = len(practices)
    # reorder practices by practice name
    practices = sorted(practices, key=lambda d: d.__dict__['name'].lower()) 
    if view != 'list':
        # append relationships to each practice
        append_relationships_multiple(practices)
    return render_template('resources.html', resources=practices, type='practice', count=count, view=view, intro_text=intro_text)

# route for displaying a single practice based on the ID in the database
@practice.route('/practices/<int:practice_id>')
def show_practice(practice_id):
    practice = get_full_resource(practice_id)
    # render Markdown as HTML
    practice.longDescription = markdown.markdown(practice.longDescription)
    practice.experimental = markdown.markdown(practice.experimental)
    practice.considerations = markdown.markdown(practice.considerations)
    practice.references = markdown.markdown(practice.references)
    return render_template('resource.html', resource=practice)

# route for editing a single practice based on the ID in the database
@practice.route('/practices/<int:practice_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_practice(practice_id):
    practice = get_resource(practice_id)
    resource_dropdown = Resource.query
    existing_relationships = get_relationships(practice_id)

    if request.method == 'POST':
        if not request.form['name']:
            flash('Name is required!')
        else:
            practice = Resource.query.get(practice_id)
            practice.name = request.form['name']
            practice.description = request.form['description']
            practice.longDescription = request.form['longDescription']
            practice.experimental = request.form['experimental']
            practice.considerations = request.form['considerations']
            practice.references = request.form['references']
            db.session.commit()
            linked_resources = request.form.getlist('linked_resources')
            remove_linked_resources = request.form.getlist('remove_linked_resources')

            edit_relationships(practice_id, linked_resources, remove_linked_resources, existing_relationships)

            return redirect(url_for('practice.get_practices',_external=True,_scheme=os.environ.get('SSL_SCHEME')))

    return render_template('edit.html', resource=practice, resource_dropdown=resource_dropdown, relationships=existing_relationships)

# route for function to delete a single practice from the edit page
@practice.route('/practices/<int:practice_id>/delete', methods=('POST',))
@login_required
def delete_practice(practice_id):
    delete_resource(practice_id)
    return redirect(url_for('practice.get_practices',_external=True,_scheme=os.environ.get('SSL_SCHEME')))
