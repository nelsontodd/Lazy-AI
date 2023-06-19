import os
from marshmallow import Schema, fields, validate, ValidationError

class LoginSchema(Schema):
    email = fields.Email()
    password = fields.Str(
        load_only=True, validate=validate.Length(min=1, max=50)
    )

class UserSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=50))
    email = fields.Email()
    password = fields.Str(
        load_only=True, validate=validate.Length(min=1, max=50)
    )

class FileSchema:

    def load(self, file):
        if file.content_type != 'application/pdf':
            raise ValidationError('Document must be a pdf.')
        if file.seek(0, os.SEEK_END) > 5242880:
            raise ValidationError('Maximum document file size 5MB.')
