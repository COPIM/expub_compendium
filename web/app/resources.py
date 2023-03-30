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

# function to retrieve data about a single resource from the database
def get_resource(resource_id):
    resource = Resource.query.filter_by(id=resource_id).first()
    if resource is None:
        abort(404)
    return resource

# function to retrieve data about a resource and its relationships
def get_full_resource(resource_id):
    resource = get_resource(resource_id)
    relationships = get_relationships(resource_id)
    for relationship in relationships:
        if relationship.type == 'tool':
            if 'tools' not in resource.__dict__.keys():
                resource.__dict__['tools'] = relationship
            elif type(resource.__dict__['tools']) == list:
                resource.__dict__['tools'].append(relationship)
            else:
                resource.__dict__['tools'] = [resource.__dict__['tools'], relationship]
        elif relationship.type == 'practice':
            if 'practices' not in resource.__dict__.keys():
                resource.__dict__['practices'] = relationship
            elif type(resource.__dict__['practices']) == list:
                resource.__dict__['practices'].append(relationship)
            else:
                resource.__dict__['practices'] = [resource.__dict__['practices'], relationship]
        elif relationship.type == 'book':
            if 'books' not in resource.__dict__.keys():
                resource.__dict__['books'] = relationship
            elif type(resource.__dict__['books']) == list:
                resource.__dict__['books'].append(relationship)
            else:
                resource.__dict__['books'] = [resource.__dict__['books'], relationship]
    if resource.type == 'book':
        book_data = get_book_data(resource.isbn)
        resource.__dict__.update(book_data)
    return resource

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
        # get highest-resolution book cover possible
        openl_url = 'https://covers.openlibrary.org/b/isbn/' + book['ISBN-13'] + '-L.jpg?default=false'
        request = requests.get(openl_url)
        if request.status_code != 200:
            book.update(cover(isbn))
        else:
            book_cover = {'thumbnail': openl_url}
            book.update(book_cover)
        return book
    except: 
        pass

# function to get full metadata for a book and combine into one object
def get_book(resource_id):
    book = get_resource(resource_id)
    book_data = get_book_data(book.isbn)
    book.__dict__.update(book_data)
    return book

# function to replace embedded URL strings with href links
def replace_urls(input):
    # Compile a regular expression to match URLs.
    # This regular expression is not exhaustive and may not match all possible URLs.
    # It is intended to be a starting point and can be refined and expanded as needed.
    url_regex = re.compile(r'((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))')

    # Find all URLs in the input string using the regular expression.
    # This will return a list of Match objects, each of which represents a single URL in the string.
    matches = url_regex.finditer(input)

    # Iterate over the list of matches and replace each URL with an HTML link.
    for match in matches:
        # Get the full URL from the Match object.
        url = match.group(0)

        # Create the HTML link by wrapping the URL in an <a> tag.
        # If the URL does not include a protocol (e.g. "http://" or "https://"),
        # then add "http://" as the default protocol.
        if not url.startswith('http'):
            link = f'<a href="http://{url}">{url}</a>'
        else:
            link = f'<a href="{url}">{url}</a>'

        # Replace the URL in the original string with the HTML link.
        input = input.replace(url, link)

    return input