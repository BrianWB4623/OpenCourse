from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import TextAreaField, FloatField
from wtforms.validators import Optional, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class SubmissionForm(FlaskForm):
    content = TextAreaField('Submission', validators=[DataRequired()], render_kw={"rows":6})
    submit = SubmitField('Submit Assignment')


class GradeForm(FlaskForm):
    score = FloatField('Score', validators=[DataRequired(), NumberRange(min=0)], default=0.0)
    feedback = TextAreaField('Feedback', validators=[Optional()], render_kw={"rows":4})
    submit = SubmitField('Save Grade')
