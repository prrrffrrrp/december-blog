from flask import abort, render_template
from flask_login import current_user

from . import home
from ..models import Post


@home.route('/')
def index():
    posts = Post.query.order_by(
        Post.timestamp.desc()).filter_by(publish=True).all()
    return render_template('index.html', posts=posts)


@home.route('/posts/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)

    try:
        if post.publish or current_user.is_admin:
            return render_template('post.html', post=post)
        else:
            abort(403)
    except AttributeError:
        abort(403)
