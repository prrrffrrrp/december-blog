from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
import bleach

# local imports:
from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    tags = db.Column(db.String(128))
    body = db.Column(db.Text(), nullable=False)
    body_html = db.Column(db.Text())
    timestamp = db.Column(db.Date(), default=datetime.utcnow)
    publish = db.Column(db.Boolean, default=False)


    @staticmethod
    def save_markdown_to_server(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes={'*': ['src']}, strip=True))

    def __repr__(self):
        return '<Post %r>' % self.title


db.event.listen(Post.body, 'set', Post.save_markdown_to_server)
