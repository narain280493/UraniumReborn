from marshmallow_sqlalchemy import ModelSchema
from models.studentapplication import studentapplication


class studentapplicationschema(ModelSchema):
    class Meta:
        model = studentapplication