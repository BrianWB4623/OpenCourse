from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    role=SelectField('Role',choices=[("student","Student"),("teacher","Teacher"),("ta","TA")],validators=[Optional()])
    submit=SubmitField('Register User')
class AssignmentForm(FlaskForm):
    name=StringField('Assignment Name',validators=[DataRequired()])
    description=TextAreaField('Assignment Description',validators=[Optional()])
    submit=SubmitField('Publish Assignment')
class MaterialForm(FlaskForm):
    name = StringField("Material Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Upload Material")





