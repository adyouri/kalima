from project.models import Comment, BlogPost
from sqlalchemy.sql.expression import func


def latest_comments():
    return Comment.query.order_by(Comment.created_date.desc()).limit(5)


def post_by_id(post_id):
    return BlogPost.query.filter_by(id = post_id).first()


def random_posts():
    return BlogPost.query.order_by(func.random()).limit(3)
