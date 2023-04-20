# @name: api.py
# @creation_date: 2023-01-12
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Exposes database data as exportable JSON for a RESTful API
# @acknowledgements:
# https://auth0.com/blog/developing-restful-apis-with-python-and-flask/
# https://stackoverflow.com/questions/59721478/serializing-sqlalchemy-with-marshmallow

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Resource, User
from .schemas import UserSchema, ToolSchema, PracticeSchema, BookSchema
from .relationships import *
import pandas as pd
import json

api = Blueprint('api', __name__)

# function to get different types from the Resource database table
def get_resource_json(resource_type):
    resources = Resource.query.filter_by(type=resource_type)
    if (resource_type=='tool'):
        resources_schema = ToolSchema(many=True)
    elif (resource_type=='practice'):
        resources_schema = PracticeSchema(many=True)
    elif (resource_type=='book'):
        resources_schema = BookSchema(many=True)
    result = resources_schema.dump(resources)
    # return all rows as a JSON array of objects
    result = jsonify(result)

    return result

# route for api page
@api.route('/api')
def api_page():
    return render_template('api.html')

# route for exporting all users in database
@api.route('/api/users')
@login_required
def get_users():
    users = User.query.all()
    users_schema = UserSchema(many=True)
    result = users_schema.dump(users)

    # return all rows as a JSON array of objects
    return jsonify(result)

# route for exporting all tools in database
@api.route('/api/tools')
def get_tools_json():
    resource_type = 'tool'
    output = get_resource_json(resource_type)
    return output

# route for exporting all practices in database
@api.route('/api/practices')
def get_practices():
    resource_type = 'practice'
    output = get_resource_json(resource_type)
    return output

# route for exporting all books in database
@api.route('/api/books')
def get_books():
    resource_type = 'book'
    output = get_resource_json(resource_type)
    return output