from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required


class PostForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    subtitle = TextAreaField('Subtitle', validators=[Required()])
    tags = StringField('Tags')
    body = TextAreaField('Post', validators=[Required()], id='post-body')
    submit = SubmitField('Save')
