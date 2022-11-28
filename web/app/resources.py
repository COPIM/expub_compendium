# @name: resources.py
# @creation_date: 2022-02-23
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: functions for resources
# @acknowledgements:

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Resource
from werkzeug.exceptions import abort
from . import db

# function to retrieve data about a single resource from the database
def get_resource(resource_id):
    resource = Resource.query.filter_by(id=resource_id).first()
    if resource is None:
        abort(404)
    return resource

# function to delete a single resource
def delete_resource(resource_id):
    deletion = Resource.query.get(resource_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')

# function to get filters for a specific field 
def get_filter_values(field):
    # get field values for filter 
    field_filter = Resource.query.filter_by(type='tool').with_entities(getattr(Resource, field))
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