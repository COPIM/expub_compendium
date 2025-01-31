# @name: resources.py
# @creation_date: 2022-02-23
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: functions for resources
# @acknowledgements:
# isbntools: https://isbntools.readthedocs.io/en/latest/info.html
# regex for URLs: https://gist.github.com/gruber/249502

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Resource
from werkzeug.exceptions import abort
from . import db
from .relationships import *
from isbntools.app import *
import requests
import re
from sqlalchemy.sql import func
import markdown

# function to retrieve data about a single resource from the database
def get_resource(resource_id):
    resource = Resource.query.filter_by(id=resource_id).first()
    if resource is None:
        abort(404)
    return resource

# function to retrieve data about a resource and its relationships
def get_full_resource(resource_id):
    resource = get_resource(resource_id)
    resource = append_relationships(resource)
    if resource.type == 'book':
        # render Markdown as HTML
        resource.description = markdown.markdown(resource.description)
        # get additional book metadata
        book_data = get_book_data(resource.isbn)
        if book_data:
            resource.__dict__.update(book_data)
    return resource

# function to get practice from Markdown file
def get_practice_markdown(practice_name, option='html'):
    file_name = practice_name.replace(" ", "_")
    with open(f'content/practices/{file_name}.md', 'r') as f:
        practice_text = f.read()
        if option == 'html':
            practice_text = markdown.markdown(practice_text)
    return practice_text

# function to write new or edited practice to Markdown file
def write_practice_markdown(practice_name, markdown):
    practice_name = practice_name.replace(" ", "_")
    with open(f'content/practices/{practice_name}.md', 'w+') as f:
        f.write(markdown)

# function to retrieve data about a curated list of resources
def get_curated_resources(resource_ids):
    resources = Resource.query.filter(Resource.id.in_(resource_ids)).order_by(func.random()).all()
    # append relationships to each resource
    append_relationships_multiple(resources)
    return resources

# function to delete a single resource
def delete_resource(resource_id):
    deletion = Resource.query.get(resource_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')

# function to get filters for a specific field 
def get_filter_values(field, type):
    # get field values for filter 
    field_filter = Resource.query.filter_by(type=type).with_entities(getattr(Resource, field))
    # turn SQLAlchemy object into list
    field_filter = [i for i, in field_filter]
    # split each element on '/' (useful for scriptingLanguage only)
    field_filter = [y for x in field_filter for y in x.split(' / ')]
    # consolidate duplicate values
    field_filter = list(dict.fromkeys(field_filter))
    # filter None values from list
    field_filter = filter(None, field_filter)
    # sort list by alphabetical order
    field_filter = sorted(field_filter)
    return field_filter

# function to get book data including metadata and covers 
def get_book_data(isbn):
    try:
        book = meta(isbn)
        description = {'desc': desc(isbn)}
        book.update(description)
        #book = get_book_cover(book)
        return book
    except: 
        pass

# function to get book cover data
def get_book_cover(book):
    # get highest-resolution book cover possible
    openl_url = 'https://covers.openlibrary.org/b/isbn/' + book['ISBN-13'] + '-L.jpg?default=false'
    request = requests.get(openl_url)
    if request.status_code != 200:
        book.update(cover(isbn))
    else:
        book_cover = {'thumbnail': openl_url}
        book.update(book_cover)
    return book