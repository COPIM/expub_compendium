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

# table for tools
class Tool(db.Model):
    __tablename__ = 'Tool'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)
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

    practice_id = db.Column(db.Integer, db.ForeignKey('Practice.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'))

    practices = db.relationship('Practice', foreign_keys=[practice_id], backref='tool')
    books = db.relationship('Book', foreign_keys=[book_id], backref='tool')

# table for practices
class Practice(db.Model):
    __tablename__ = 'Practice'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.Text)
    description = db.Column(db.Text)

    tool_id = db.Column(db.Integer, db.ForeignKey('Tool.id'))
    typology_id = db.Column(db.Integer, db.ForeignKey('Typology.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('Reference.id'))

    tools = db.relationship('Tool', foreign_keys=[tool_id], backref='practice')
    typologies = db.relationship('Typology', foreign_keys=[typology_id], backref='practice')
    books = db.relationship('Book', foreign_keys=[book_id], backref='practice')
    references = db.relationship('Reference', foreign_keys=[reference_id], backref='practice')

# table for sensitivities
class Sensitivity(db.Model):
    __tablename__ = 'Sensitivity'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.Text)
    description = db.Column(db.Text)

    practice_id = db.Column(db.Integer, db.ForeignKey('Practice.id'))
    typology_id = db.Column(db.Integer, db.ForeignKey('Typology.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('Reference.id'))

    practices = db.relationship('Practice', foreign_keys=[practice_id], backref='sensitivity')
    typologies = db.relationship('Typology', foreign_keys=[typology_id], backref='sensitivity')
    references = db.relationship('Reference', foreign_keys=[reference_id], backref='sensitivity')

# table for typologies
class Typology(db.Model):
    __tablename__ = 'Typology'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.Text)
    description = db.Column(db.Text)

    tool_id = db.Column(db.Integer, db.ForeignKey('Tool.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'))
    practice_id = db.Column(db.Integer, db.ForeignKey('Practice.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('Reference.id'))

    tools = db.relationship('Tool', foreign_keys=[tool_id], backref='typology')
    books = db.relationship('Book', foreign_keys=[book_id], backref='typology_books')
    practices = db.relationship('Practice', foreign_keys=[practice_id], backref='typology')
    references = db.relationship('Reference', foreign_keys=[reference_id], backref='typology')

# table for workflows
class Workflow(db.Model):
    __tablename__ = 'Workflow'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)

# table for publishers
class Publisher(db.Model):
    __tablename__ = 'Publisher'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    publisherUrl = db.Column(db.Text)

    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'))

    books = db.relationship('Book', foreign_keys=[book_id], backref='publisher')

# table for books
class Book(db.Model):
    __tablename__ = 'Book'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.Text)
    description = db.Column(db.Text)

    tool_id = db.Column(db.Integer, db.ForeignKey('Tool.id'))
    typology_id = db.Column(db.Integer, db.ForeignKey('Typology.id'))
    practice_id = db.Column(db.Integer, db.ForeignKey('Practice.id'))
    workflow_id = db.Column(db.Integer, db.ForeignKey('Workflow.id'))

    tools = db.relationship('Tool', foreign_keys=[tool_id], backref='book')
    typology = db.relationship('Typology', foreign_keys=[typology_id], backref='book')
    practices = db.relationship('Practice', foreign_keys=[practice_id], backref='book')
    workflow = db.relationship('Workflow', foreign_keys=[workflow_id], backref='book')

# table for references
class Reference(db.Model):
    __tablename__ = 'Reference'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    created = db.Column(db.DateTime, default=datetime.utcnow)
    zoteroUrl = db.Column(db.Text)
