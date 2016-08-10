from project import db
from models import BlogPost, User
db.create_all()

db.session.add(User("admin", "ad@min", "admin"))
db.session.commit()

db.session.add(BlogPost("Good", "I\'m good.", 1))
db.session.add(BlogPost("Well", "I\'m well.", 1))
db.session.add(BlogPost("Postgres", "I\'m PostgreSQL.", 1))
db.session.commit()
