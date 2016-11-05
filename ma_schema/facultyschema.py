from marshmallow_sqlalchemy import ModelSchema
from models.faculty import faculty


class facultyschema(ModelSchema):
    class Meta:
        model = faculty

