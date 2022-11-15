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
    field_filter = Resource.query.filter_by(type='tool').with_entities(getattr(Resource, field))
    field_filter = [i for i, in field_filter]
    field_filter = list(dict.fromkeys(field_filter))
    field_filter = filter(None, field_filter)
    field_filter = sorted(field_filter)
    return field_filter