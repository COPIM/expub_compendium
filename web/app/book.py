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
import os
from sqlalchemy.sql import func
import markdown

book = Blueprint('book', __name__)

# route for displaying all books in database
@book.route('/books')
def get_books():
    # GET PARAMETERS
    # get URL parameters for views and pages
    view = request.args.get('view')
    page = request.args.get('page', 1, type=int)
    # set resource type
    resource_type = 'book'
    # get introductory paragraph Markdown
    with open('content/books.md', 'r') as f:
        intro_text = f.read()
        intro_text = markdown.markdown(intro_text)

    # DATABASE QUERY
    books_query = Resource.query.filter_by(type=resource_type)

    # FILTERING
    for key in request.args.keys():
        if key != 'view' and key != 'page':
            if (key == 'practice' and request.args.get(key) != ''):
                books_1 = books_query.join(Relationship, Relationship.first_resource_id == Resource.id, isouter=True).filter(Relationship.second_resource_id==request.args.get(key))
                books_2 = books_query.join(Relationship, Relationship.second_resource_id == Resource.id, isouter=True).filter(Relationship.first_resource_id==request.args.get(key))
                books_query = books_1.union(books_2)
            if (key != 'practice' and request.args.get(key) != ''):
                kwargs = {key: request.args.get(key)}
                books_query = books_query.filter_by(**kwargs)

    # finalise the query and add pagination
    books = books_query.order_by(Resource.name).paginate(page=page, per_page=25)

    # FILTERS MENU
    # get values for filter menu dropdowns
    # practices 
    practices_filter = Resource.query.filter_by(type='practice').with_entities(Resource.id, Resource.name).all()
    # year
    year_filter = get_filter_values('year', resource_type)
    # typology
    typology_filter = get_filter_values('typology', resource_type)

    # POST-FILTERING PROCESSING
    # if view is 'expanded' then append relationships
    if view != 'list':
        # append relationships to each book
        append_relationships_multiple_paginated(books)
    # render Markdown as HTML
    for book in books:
        book.description = markdown.markdown(book.description)
        
    return render_template('resources.html', resources=books, type=resource_type, practices_filter=practices_filter, year_filter=year_filter, typology_filter=typology_filter, view=view, page=page, intro_text=intro_text)

# route for displaying a single book based on the ID in the database
@book.route('/books/<int:book_id>')
def show_book(book_id):
    book = get_full_resource(book_id)
    return render_template('book.html', resource=book)

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
