from marshmallow_sqlalchemy import ModelSchema
from models.overrides import overrides


class overrideschema(ModelSchema):
    class Meta:
        model = overrides
