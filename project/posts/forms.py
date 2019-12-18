from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(max=100)])
    description = TextAreaField('description', validators = [DataRequired()])
    category = StringField('category', validators = [DataRequired()])
    tags = StringField('tags', validators = [DataRequired()])

class EditPostForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(max=100)])
    description = TextAreaField('description', validators = [DataRequired()])
    category = StringField('category', validators = [DataRequired()])
    tags = StringField('tags', validators = [DataRequired()])

class CommentForm(FlaskForm):
    content = TextAreaField('content', validators = [DataRequired(), Length(max=10000)])
