from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = TextAreaField('Subtitle', validators=[DataRequired()])
    tags = StringField('Tags')
    body = TextAreaField('Post', validators=[DataRequired()], id='post-body')
    submit = SubmitField('Save')


