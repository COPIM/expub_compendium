# @name: book.py
# @creation_date: 2022-04-05
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: book route for book-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .resources import *
from .relationships import *
from . import db
from sqlalchemy import text
import os

book = Blueprint('book', __name__)

# route for displaying all books in database
@book.route('/books')
def get_books():
    type = 'book'
    books = Resource.query.filter_by(type=type)
    for key in request.args.keys():
        if key == 'practice':
            query = 'SELECT Resource.* FROM Resource LEFT JOIN Relationship ON Resource.id=Relationship.first_resource_id WHERE Relationship.second_resource_id=' + request.args.get(key) + ' AND Resource.type="' + type + '";'
            with db.engine.connect() as conn:
                books = conn.execute(text(query))
        else:
            kwargs = {'type': type, key: request.args.get(key)}
            books = Resource.query.filter_by(**kwargs)
    # get filters
    # practices 
    practices_filter = Resource.query.filter_by(type='practice').with_entities(Resource.id, Resource.name)
    # year
    year_filter = get_filter_values('year', type)
    # typology
    typology_filter = get_filter_values('typology', type)
    return render_template('resources.html', resources=books, type=type, practices_filter=practices_filter, year_filter=year_filter, typology_filter=typology_filter)

# route for displaying a single book based on the ID in the database
@book.route('/books/<int:book_id>')
def show_book(book_id):
    book = get_resource(book_id)
    relationships = get_relationships(book_id)
    book_data = get_book_data(book.isbn)
    return render_template('book.html', resource=book, relationships=relationships, book=book_data)

# route for editing a single book based on the ID in the database
@book.route('/books/<int:book_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_book(book_id):
    book = get_resource(book_id)
    resource_dropdown = Resource.query
    existing_relationships = get_relationships(book_id)

    if request.method == 'POST':
        if not request.form['name']:
            flash('Name is required!')
        else:
            book = Resource.query.get(book_id)
            book.name = request.form['name']
            book.description = request.form['description']
            book.author = request.form['author']
            book.year = request.form['year']
            book.bookUrl = request.form['bookUrl']
            book.isbn = request.form['isbn']
            book.typology = request.form['typology']
            db.session.commit()
            linked_resources = request.form.getlist('linked_resources')
            remove_linked_resources = request.form.getlist('remove_linked_resources')

            edit_relationships(book_id, linked_resources, remove_linked_resources, existing_relationships)

            return redirect(url_for('book.get_books',_external=True,_scheme=os.environ.get('SSL_SCHEME')))

    return render_template('edit.html', resource=book, resource_dropdown=resource_dropdown, relationships=existing_relationships)


# route for function to delete a single book from the edit page
@book.route('/books/<int:book_id>/delete', methods=('POST',))
@login_required
def delete_book(book_id):
    delete_resource(book_id)
    return redirect(url_for('book.get_books',_external=True,_scheme=os.environ.get('SSL_SCHEME')))
