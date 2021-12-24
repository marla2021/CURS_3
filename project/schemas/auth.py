from marshmallow import fields, Schema


class AuthSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
