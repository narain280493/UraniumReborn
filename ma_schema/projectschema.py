from marshmallow_sqlalchemy import ModelSchema
from models.project import project


class projectschema(ModelSchema):
    class Meta:
        model = project
