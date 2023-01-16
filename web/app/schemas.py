# @name: schemas.py
# @creation_date: 2023-01-16
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Data schemas for API export
# @acknowledgements:

from . import ma
from marshmallow import Schema

# schema for JSON transformation of User table via Marshmallow
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'name')
        ordered = True

# schema for JSON transformation of Resource table via Marshmallow
class ToolSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'developer', 'developerUrl', 'projectUrl', 'repositoryUrl', 'license', 'scriptingLanguage', 'expertiseToUse', 'expertiseToHost', 'dependencies', 'ingestFormats', 'outputFormats', 'status')
        ordered = True

class PracticeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'experimental', 'lessonsLearned', 'references')
        ordered = True

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'author', 'year', 'bookUrl', 'isbn')
        ordered = True

# subschemas for nested fields
class DeveloperSchema(ma.Schema):
    class Meta:
        fields = ('developer', 'developerUrl')
        ordered = True
