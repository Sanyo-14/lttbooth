from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class CommentForm(FlaskForm):
    content = TextAreaField('Leave a comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class AddBehaviourForm(FlaskForm):
    name = StringField('Behaviour Name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Add Behaviour')