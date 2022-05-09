# @name: resources.py
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
def get_linked_resources(primary_id):
    primary_relationships = Relationship.query.filter_by(first_resource_id=primary_id).all()
    links = []
    if primary_relationships:
        links = []
        for relationship in primary_relationships:
             secondary_id = relationship.second_resource_id
             links.extend(Resource.query.filter_by(id=secondary_id).all())
        secondary_relationships = Relationship.query.filter_by(second_resource_id=primary_id).all()
        if secondary_relationships:
            for relationship in secondary_relationships:
                primary_id = relationship.first_resource_id
                links.extend(Resource.query.filter_by(id=primary_id).all())
        return links
    else:
        secondary_relationships = Relationship.query.filter_by(second_resource_id=primary_id).all()
        if secondary_relationships:
            links = []
            for relationship in secondary_relationships:
                primary_id = relationship.first_resource_id
                links.extend(Resource.query.filter_by(id=primary_id).all())
            return links

# function to add a relationship to a linked resource
def add_linked_resource(resource_id, linked_resource_id):
    first_resource_id = resource_id
    second_resource_id = linked_resource_id
    new_relationship = Relationship(first_resource_id=first_resource_id, second_resource_id=second_resource_id)

    # add the new relationship to the database
    db.session.add(new_relationship)
    db.session.commit()

# function to delete a single resource
def delete_resource(resource_id):
    deletion = Resource.query.get(resource_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')
