from marshmallow_sqlalchemy import ModelSchema
from models.loginpage import loginpage


class loginpageschema(ModelSchema):
    class Meta:
        model = loginpage
