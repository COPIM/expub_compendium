# @name: schemas.py
# @creation_date: 2023-01-16
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Data schemas for API export
# @acknowledgements:
# https://marshmallow.readthedocs.io/en/stable/quickstart.html#next-steps
# https://stackoverflow.com/questions/59721478/serializing-sqlalchemy-with-marshmallow

from . import ma
import os
from marshmallow import Schema, fields, post_dump
from flask_marshmallow import Marshmallow

# schema for JSON transformation of User table via Marshmallow
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'name')
        ordered = True

# schema for JSON transformation of Resource table via Marshmallow
class ToolSchema(ma.Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    developer = fields.Str()
    developerUrl = fields.Str()
    projectUrl = fields.Str()
    repositoryUrl = fields.Str()
    license = fields.Str()
    scriptingLanguage = fields.Str()
    expertiseToUse = fields.Str()
    expertiseToHost = fields.Str()
    dependencies = fields.Str()
    ingestFormats = fields.Str()
    outputFormats = fields.Str()
    videoUrl = fields.Str()
    status = fields.Str()
    class Meta:
        ordered = True

class PracticeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'content')
        ordered = True

    id = fields.Int(required=True)
    name = fields.Str(required=True)
    content = fields.Str(dump_only=True)  # Will store the Markdown content

    @post_dump
    def load_markdown(self, data, **kwargs):
        practice_name = data['name'].replace(" ", "_")
        # Reads the markdown content based on the name field after serialization.
        file_path = f"content/practices/{practice_name}.md"  # Adjust the path as needed
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data["content"] = file.read()
        else:
            data["content"] = "Markdown file not found."
        return data

class BookSchema(ma.Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    author = fields.Str()
    year = fields.Str()
    bookUrl = fields.Str()
    videoUrl = fields.Str()
    isbn = fields.Str()
    class Meta:
        ordered = True

# subschemas for nested fields
class DeveloperSchema(ma.Schema):
    class Meta:
        fields = ('developer', 'developerUrl')
        ordered = True
