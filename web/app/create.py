# @name: create.py
# @version: 0.1
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

                if request.form.get('linked_practice_id'):
                    tool = Resource.query.filter_by(type='tool').filter_by(name=name).first()
                    first_resource_id = tool.id
                    second_resource_id = request.form.get('linked_practice_id')
                    new_relationship = Relationship(first_resource_id=first_resource_id, second_resource_id=second_resource_id)

                    # add the new relationship to the database
                    db.session.add(new_relationship)
                    db.session.commit()

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

        elif request.form.get('resource_type') == 'sensitivity':
            type = 'sensitivity'
            name = request.form.get('sensitivity_name')
            description = request.form.get('description')

            if not name:
                flash('Name is required!')
            else:
                sensitivity = Sensitivity.query.filter_by(name=name).first() # if this returns a sensitivity, then the name already exists in database

                if sensitivity: # if a sensitivity is found, we want to redirect back to create page
                    flash('Sensitivity with same name already exists')
                    return redirect(url_for('create.create_resource'))

                # create a new sensitivity with the form data
                new_sensitivity = Resource(type=type, name=name, description=description)

                # add the new sensitivity to the database
                db.session.add(new_sensitivity)
                db.session.commit()

        elif request.form.get('resource_type') == 'typology':
            type = 'typology'
            name = request.form.get('typology_name')
            description = request.form.get('description')

            if not name:
                flash('Name is required!')
            else:
                typology = Typology.query.filter_by(name=name).first() # if this returns a typology, then the name already exists in database

                if typology: # if a typology is found, we want to redirect back to create page
                    flash('Typology with same name already exists')
                    return redirect(url_for('create.create_resource'))

                # create a new typology with the form data
                new_typology = Resource(type=type, name=name, description=description)

                # add the new typology to the database
                db.session.add(new_typology)
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

        elif request.form.get('resource_type') == 'reference':
            type = 'reference'
            zoteroUrl = request.form.get('zoteroUrl')

            if not zoteroUrl:
                flash('Zotero URL is required!')
            else:
                reference = Reference.query.filter_by(zoteroUrl=zoteroUrl).first() # if this returns a reference, then the name already exists in database

                if reference: # if a reference is found, we want to redirect back to create page
                    flash('Reference with same URL already exists')
                    return redirect(url_for('create.create_resource'))

                # create a new reference with the form data
                new_reference = Resource(type=type, zoteroUrl=zoteroUrl)

                # add the new reference to the database
                db.session.add(new_reference)
                db.session.commit()

    practice_dropdown = Resource.query.filter_by(type='practice')
    return render_template('create.html', practice_dropdown=practice_dropdown)
