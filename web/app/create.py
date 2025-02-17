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
from .relationships import *
from . import db
import os

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
            developer = request.form.get('developer')
            developerUrl = request.form.get('developerUrl')
            projectUrl = request.form.get('projectUrl')
            repositoryUrl = request.form.get('repositoryUrl')
            license = request.form.get('license')
            scriptingLanguage = request.form.get('scriptingLanguage')
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
                    return redirect(url_for('create.create_resource',_external=True,_scheme=os.environ.get('SSL_SCHEME')))

                # create a new tool with the form data
                new_tool = Resource(type=type, name=name, description=description, developer=developer, developerUrl=developerUrl, projectUrl=projectUrl, repositoryUrl=repositoryUrl, license=license, scriptingLanguage=scriptingLanguage, expertiseToUse=expertiseToUse, expertiseToHost=expertiseToHost, dependencies=dependencies, ingestFormats=ingestFormats, outputFormats=outputFormats, status=status)

                # add the new tool to the database
                db.session.add(new_tool)
                db.session.commit()

                if request.form.getlist('linked_practices') or request.form.getlist('linked_books'):
                    linked_resources = request.form.getlist('linked_practices') + request.form.getlist('linked_books')
                    for linked_resource in linked_resources:
                        tool = Resource.query.filter_by(type='tool').filter_by(name=name).first()
                        add_relationship(tool.id, linked_resource)

        elif request.form.get('resource_type') == 'practice':
            type = 'practice'
            name = request.form.get('practice_name')
            practice_markdown = request.form.get('practice_markdown')

            if not name:
                flash('Name is required!')
            else:
                practice = Resource.query.filter_by(type='practice').filter_by(name=name).first() # if this returns a practice, then the name already exists in database

                if practice: # if a practice is found, we want to redirect back to create page
                    flash('Practice with same name already exists')
                    return redirect(url_for('create.create_resource',_external=True,_scheme=os.environ.get('SSL_SCHEME')))

                # create a new practice with the form data
                new_practice = Resource(type=type, name=name)
                # add the new practice to the database
                db.session.add(new_practice)
                db.session.commit()

                write_practice_markdown(name, practice_markdown)

                if request.form.getlist('linked_tools') or request.form.getlist('linked_books'):
                    linked_resources = request.form.getlist('linked_tools') + request.form.getlist('linked_books')
                    for linked_resource in linked_resources:
                        practice = Resource.query.filter_by(type='practice').filter_by(name=name).first()
                        add_relationship(practice.id, linked_resource)

        elif request.form.get('resource_type') == 'book':
            type = 'book'
            name = request.form.get('book_name')
            description = request.form.get('description')
            author = request.form.get('author')
            year = request.form.get('year')
            typology = request.form.get('typology')
            bookUrl = request.form.get('bookUrl')
            isbn = request.form.get('isbn')

            if not name:
                flash('Name is required!')
            else:
                book = Resource.query.filter_by(type='book').filter_by(name=name).first() # if this returns a book, then the name already exists in database

                if book: # if a book is found, we want to redirect back to create page
                    flash('Book with same name already exists')
                    return redirect(url_for('create.create_resource',_external=True,_scheme=os.environ.get('SSL_SCHEME')))

                # create a new book with the form data
                new_book = Resource(type=type, name=name, description=description, author=author, year=year, typology=typology, bookUrl=bookUrl, isbn=isbn)

                # add the new book to the database
                db.session.add(new_book)
                db.session.commit()

                if request.form.getlist('linked_tools') or request.form.getlist('linked_practices'):
                    linked_resources = request.form.getlist('linked_tools') + request.form.getlist('linked_practices')
                    for linked_resource in linked_resources:
                        book = Resource.query.filter_by(type='book').filter_by(name=name).first()
                        add_relationship(book.id, linked_resource)

    resource_dropdown = Resource.query.order_by(Resource.name)
    return render_template('create.html', resource_dropdown=resource_dropdown)
