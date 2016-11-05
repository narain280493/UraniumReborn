from marshmallow_sqlalchemy import ModelSchema
from models.fileurl import fileurl


class fileurlschema(ModelSchema):
    class Meta:
        model = fileurl