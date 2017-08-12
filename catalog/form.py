from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Please enter your username.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])

class SigninForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Please enter your username.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])