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
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# table for tools
class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    project_url = db.Column(db.Text)
    repository_url = db.Column(db.Text)
    platform_status = db.Column(db.Text)
    expertise = db.Column(db.Text)
    self_host_expertise = db.Column(db.Text)
    ingest = db.Column(db.Text)
    output = db.Column(db.Text)
    saas = db.Column(db.Text)
    dependencies = db.Column(db.Text)

# table for examples
class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.Text)
    description = db.Column(db.Text)

# table for examples
class Practice(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
