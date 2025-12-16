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
    title=StringField('Assignment Title',validators=[DataRequired()])
    description=TextAreaField('Assignment Description',validators=[DataRequired()])
    submit=SubmitField('Publish Assignment')
class MaterialForm(FlaskForm):
    title = StringField("Material Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Upload Material")


class SubmissionForm(FlaskForm):
    content = TextAreaField('Submission', validators=[DataRequired()])
    submit = SubmitField('Submit Assignment')


class GradeForm(FlaskForm):
    score = StringField('Score', validators=[DataRequired()])
    feedback = TextAreaField('Feedback', validators=[Optional()])
    submit = SubmitField('Save Grade')





