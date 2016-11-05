from marshmallow_sqlalchemy import ModelSchema
from models.student import student


class studentschema(ModelSchema):
    class Meta:
        model = student
