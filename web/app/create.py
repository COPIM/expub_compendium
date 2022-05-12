# @name: create.py
# @creation_date: 2021-10-25
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: create route for creating tools, examples, and practices
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .models import Relationship
from .resources import *
from werkzeug.exceptions import abort
from . import db

create = Blueprint('create', __name__)

# route for creating a new resource
@create.route('/create', methods=('GET', 'POST'))
@login_required
def create_resource():
    if request.method == 'POST':
        if request.form.get('resource_type') == 'tool':
            type = 'tool'
            name = request.form.get('tool_name')
            description = request.form.get('description')
            projectUrl = request.form.get('projectUrl')
            repositoryUrl = request.form.get('repositoryUrl')
            expertiseToUse = request.form.get('expertiseToUse')
            expertiseToHost = request.form.get('expertiseToHost')
            dependencies = request.form.get('dependencies')
            ingestFormats = request.form.get('ingestFormats')
            outputFormats = request.form.get('outputFormats')
            status = request.form.get('status')

            if not name:
                flash('Name is required!')
            else:
                tool = Resource.query.filter_by(type='tool').filter_by(name=name).first() # if this returns a tool, then the name already exists in database

                if tool: # if a tool is found, we want to redirect back to create page
                    flash('Tool with same name already exists')
                    return redirect(url_for('create.create_resource'))

                # create a new tool with the form data
                new_tool = Resource(type=type, name=name, description=description, projectUrl=projectUrl, repositoryUrl=repositoryUrl, expertiseToUse=expertiseToUse, expertiseToHost=expertiseToHost, dependencies=dependencies, ingestFormats=ingestFormats, outputFormats=outputFormats, status=status)

                # add the new tool to the database
                db.session.add(new_tool)
                db.session.commit()

                if request.form.getlist('linked_resources'):
                    for linked_resource in request.form.getlist('linked_resources'):
                        tool = Resource.query.filter_by(type='tool').filter_by(name=name).first()
                        add_linked_resource(tool.id, linked_resource)

        elif request.form.get('resource_type') == 'practice':
            type = 'practice'
            name = request.form.get('practice_name')
            description = request.form.get('description')

            if not name:
                flash('Name is required!')
            else:
                practice = Resource.query.filter_by(type='practice').filter_by(name=name).first() # if this returns a practice, then the name already exists in database

                if practice: # if a practice is found, we want to redirect back to create page
                    flash('Practice with same name already exists')
                    return redirect(url_for('create.create_resource'))

                # create a new practice with the form data
                new_practice = Resource(type=type, name=name, description=description)

                # add the new practice to the database
                db.session.add(new_practice)
                db.session.commit()

        elif request.form.get('resource_type') == 'publisher':
            type = 'publisher'
            name = request.form.get('publisher_name')
            description = request.form.get('description')
            publisherUrl = request.form.get('publisherUrl')

            if not name:
                flash('Name is required!')
            else:
                publisher = Publisher.query.filter_by(name=name).first() # if this returns a publisher, then the name already exists in database

                if publisher: # if a publisher is found, we want to redirect back to create page
                    flash('Publisher with same name already exists')
                    return redirect(url_for('create.create_resource'))

                # create a new publisher with the form data
                new_publisher = Resource(type=type, name=name, description=description, publisherUrl=publisherUrl)

                # add the new publisher to the database
                db.session.add(new_publisher)
                db.session.commit()

        elif request.form.get('resource_type') == 'book':
            type = 'book'
            name = request.form.get('book_name')
            description = request.form.get('description')

            if not name:
                flash('Name is required!')
            else:
                book = Book.query.filter_by(name=name).first() # if this returns a book, then the name already exists in database

                if book: # if a book is found, we want to redirect back to create page
                    flash('Book with same name already exists')
                    return redirect(url_for('create.create_resource'))

                # create a new book with the form data
                new_book = Resource(type=type, name=name, description=description)

                # add the new book to the database
                db.session.add(new_book)
                db.session.commit()

    resource_dropdown = Resource.query
    return render_template('create.html', resource_dropdown=resource_dropdown)
