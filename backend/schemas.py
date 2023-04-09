from marshmallow import Schema, fields, validate

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
