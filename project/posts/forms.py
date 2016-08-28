from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(Form):
    title = TextField('title', validators = [DataRequired(), Length(max=100)])
    description = TextAreaField('description', validators = [DataRequired()])
    category = TextField('category', validators = [DataRequired()])
    tags = TextField('tags', validators = [DataRequired()])


class CommentForm(Form):
    content = TextAreaField('content', validators = [DataRequired()])
