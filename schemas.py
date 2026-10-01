from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    done = fields.Bool(load_default=False)
