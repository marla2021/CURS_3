from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Int()


class UserValidatorSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class JWTTokensValidatore(Schema):
    access_token = fields.String()
    refresh_token = fields.String(required=True)
