from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired,Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    role=StringField('Role',validators=[Optional()])
    submit=SubmitField('Register User')
class AssignmentForm(FlaskForm):
    name=StringField('Assignment Name',validators=[DataRequired()])
    description=TextAreaField('Assignment Description',validators=[Optional()])
    submit=SubmitField('Publish Assignment')




