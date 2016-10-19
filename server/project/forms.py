from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class SignupForm(Form):
    first_name = StringField('First Name', validators=[DataRequired("Please fill in your first name")])
    last_name = StringField('Last Name', validators=[DataRequired("Please fill in your last name")])
    email = StringField('Email', validators=[DataRequired("Please fill in your email address")])
    password = PasswordField('Password', validators=[DataRequired("Please fill in your first name")])
    submit = SubmitField('Signup')