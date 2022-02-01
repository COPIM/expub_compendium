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
from .models import Tool
from .models import Book
from .models import Practice
from werkzeug.exceptions import abort
from . import db

create = Blueprint('create', __name__)

# route for creating a new resource
@create.route('/create', methods=('GET', 'POST'))
@login_required
def create_resource():
    if request.method == 'POST':
        if request.form.get('resource_type') == 'tool':
            name = request.form.get('name')
            description = request.form.get('description')
            project_url = request.form.get('project_url')
            repository_url = request.form.get('repository_url')
            platform_status = request.form.get('platform_status')
            expertise = request.form.get('expertise')
            self_host_expertise = request.form.get('self_host_expertise')
            ingest = request.form.get('ingest')
            output = request.form.get('output')
            saas = request.form.get('saas')
            dependencies = request.form.get('dependencies')

            if not name:
                flash('Name is required!')
            else:
                tool = Tool.query.filter_by(name=name).first() # if this returns a tool, then the name already exists in database

                if tool: # if a tool is found, we want to redirect back to create page
                    flash('Tool with same name already exists')
                    return redirect(url_for('create.create'))

                # create a new tool with the form data
                new_tool = Tool(name=name, description=description, project_url=project_url, repository_url=repository_url, platform_status=platform_status, expertise=expertise, self_host_expertise=self_host_expertise, ingest=ingest, output=output, saas=saas, dependencies=dependencies)

                # add the new tool to the database
                db.session.add(new_tool)
                db.session.commit()

        elif request.form.get('resource_type') == 'book':
            name = request.form.get('name')
            description = request.form.get('description')

            if not name:
                flash('Name is required!')
            else:
                example = Book.query.filter_by(name=name).first() # if this returns a book, then the name already exists in database

                if example: # if a book is found, we want to redirect back to create page
                    flash('Book with same name already exists')
                    return redirect(url_for('create.create'))

                # create a new book with the form data
                new_book = Book(name=name, description=description)

                # add the new book to the database
                db.session.add(new_book)
                db.session.commit()

        elif request.form.get('resource_type') == 'practice':
            name = request.form.get('name')
            description = request.form.get('description')

            if not name:
                flash('Name is required!')
            else:
                practice = Practice.query.filter_by(name=name).first() # if this returns a practice, then the name already exists in database

                if practice: # if a practice is found, we want to redirect back to create page
                    flash('Practice with same name already exists')
                    return redirect(url_for('create.create'))

                # create a new practice with the form data
                new_practice = Practice(name=name, description=description)

                # add the new practice to the database
                db.session.add(new_practice)
                db.session.commit()

    return render_template('create.html')
