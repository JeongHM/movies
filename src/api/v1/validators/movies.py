from marshmallow import Schema, fields
from marshmallow.validate import Length


class MovieSchema(Schema):
    name = fields.String(required=True, allow_none=False, validate=Length(
        min=1))
    genre = fields.String(required=True, allow_none=False, validate=Length(
        min=1))
    grade = fields.Integer(required=True, allow_none=False)
    views = fields.Integer(required=True, default=0, allow_none=True)
    release_at = fields.Date(required=True, allow_none=False,)