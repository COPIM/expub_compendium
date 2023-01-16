# @name: api.py
# @creation_date: 2023-01-12
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Exposes database data as exportable JSON for an API
# @acknowledgements:

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Resource, User
from .schemas import UserSchema, ToolSchema, PracticeSchema, BookSchema

api = Blueprint('api', __name__)

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
def get_tools():
    type = 'tool'
    resources = Resource.query.filter_by(type=type)
    resources_schema = ToolSchema(many=True)
    result = resources_schema.dump(resources)

    # return all rows as a JSON array of objects
    return jsonify(result)

# route for exporting all practices in database
@api.route('/api/practices')
def get_practices():
    type = 'practice'
    resources = Resource.query.filter_by(type=type)
    resources_schema = PracticeSchema(many=True)
    result = resources_schema.dump(resources)

    # return all rows as a JSON array of objects
    return jsonify(result)

# route for exporting all books in database
@api.route('/api/books')
def get_books():
    type = 'book'
    resources = Resource.query.filter_by(type=type)
    resources_schema = BookSchema(many=True)
    result = resources_schema.dump(resources)

    # return all rows as a JSON array of objects
    return jsonify(result)