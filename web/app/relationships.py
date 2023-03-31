# @name: relationships.py
# @creation_date: 2022-04-11
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: functions for relationships
# @acknowledgements:

from .models import Resource
from .models import Relationship
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

# function to append relationships to a resource object
def append_relationships(resource):
    relationships = get_relationships(resource.id)
    if relationships:
        for relationship in relationships:
            if relationship.type == 'tool':
                if 'tools' not in resource.__dict__.keys():
                    resource.__dict__['tools'] = []
                    resource.__dict__['tools'].append(relationship)
                else:
                    resource.__dict__['tools'].append(relationship)
            elif relationship.type == 'practice':
                if 'practices' not in resource.__dict__.keys():
                    resource.__dict__['practices'] = []
                    resource.__dict__['practices'].append(relationship)
                else:
                    resource.__dict__['practices'].append(relationship)
            elif relationship.type == 'book':
                if 'books' not in resource.__dict__.keys():
                    resource.__dict__['books'] = []
                    resource.__dict__['books'].append(relationship)
                else:
                    resource.__dict__['books'].append(relationship)
        return resource
    else:
        return resource

# function to append relationships to a dictionary of resources
def append_relationships_multiple(resources):
    for index, resource in enumerate(resources):
        resources[index] = append_relationships(resource)
    return resources

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
    
# logic for editing relationships 
def edit_relationships(resource_id, linked_resources, remove_linked_resources, existing_relationships):
    if linked_resources:
        for linked_resource in linked_resources:
            link = Resource.query.get(linked_resource)
            if existing_relationships and link not in existing_relationships:
                add_relationship(resource_id, linked_resource)
            elif not existing_relationships:
                add_relationship(resource_id, linked_resource)
    if remove_linked_resources:
        for remove_linked_resource in remove_linked_resources:
            delete_relationship(resource_id, remove_linked_resource)
