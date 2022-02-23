# @name: models.py
# @version: 0.1
# @creation_date: 2021-10-20
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Database models for tables in the database
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

from flask_login import UserMixin
from . import db
from datetime import datetime

# table for users
class User(UserMixin, db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# table for resources
class Resource(db.Model):
    __tablename__ = 'Resource'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.Text)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    projectUrl = db.Column(db.Text)
    repositoryUrl = db.Column(db.Text)
    expertiseToUse = db.Column(db.Text)
    expertiseToHost = db.Column(db.Text)
    dependencies = db.Column(db.Text)
    ingestFormats = db.Column(db.Text)
    outputFormats = db.Column(db.Text)
    status = db.Column(db.Text)
    publisherUrl = db.Column(db.Text)
    zoteroUrl = db.Column(db.Text)

# table for relationships
class Relationships(db.Model):
    __tablename__ = 'Relationships'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    first_resource_id = db.Column(db.Integer)
    second_resource_id = db.Column(db.Integer)
