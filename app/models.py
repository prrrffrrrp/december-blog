from datetime import datetime
from app import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    subtitle = db.Column(db.Text(), nullable=False)
    tags = db.Column(db.String(128))
    body = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.Date(), default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.title
