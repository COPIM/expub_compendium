# @name: resources.py
# @version: 0.1
# @creation_date: 2022-02-23
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: functions for resources
# @acknowledgements:

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from .models import Relationship
from werkzeug.exceptions import abort
from . import db

# function to retrieve data about a single resource from the database
def get_resource(resource_id):
    resource = Resource.query.filter_by(id=resource_id).first()
    if resource is None:
        abort(404)
    return resource

# function to retrieve linked resources
def get_linked_resources(resource_id):
    relationships = Relationship.query.filter_by(first_resource_id=resource_id).first()
    if relationships:
        resource_id = relationships.second_resource_id
        resources = Resource.query.filter_by(id=resource_id).all()
        return resources

# function to delete a single resource
def delete_resource(resource_id):
    deletion = Resource.query.get(resource_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')
