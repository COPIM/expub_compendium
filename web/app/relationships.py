# @name: relationships.py
# @creation_date: 2022-04-11
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: functions for relationships
# @acknowledgements:

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Resource
from .models import Relationship
from werkzeug.exceptions import abort
from . import db

# function to retrieve linked resources
def get_relationships(primary_id):
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
def add_relationship(resource_id, linked_resource_id):
    first_resource_id = resource_id
    second_resource_id = linked_resource_id
    new_relationship = Relationship(first_resource_id=first_resource_id, second_resource_id=second_resource_id)

    # add the new relationship to the database
    db.session.add(new_relationship)
    db.session.commit()

# function to delete a single relationship
def delete_relationship(main_id, for_deletion_id):
    relation = Relationship.query.filter(((Relationship.first_resource_id == main_id) & (Relationship.second_resource_id == for_deletion_id)) | ((Relationship.first_resource_id == for_deletion_id) & (Relationship.second_resource_id == main_id))).first()
    deletion = Relationship.query.get(relation.id)
    db.session.delete(deletion)
    db.session.commit()
