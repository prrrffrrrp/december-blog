from flask import abort, render_template
from flask_login import current_user

from . import home
from ..models import Post


@home.route('/')
def index():
    posts = Post.query.order_by(
        Post.timestamp.desc()).filter_by(publish=True).all()

    # This asks the database for tags and returns a list of tuples:
    # tags = Post.query.with_entities(Post.tags).all()

    tags = [post.tags.split(',') for post in posts]
    tags = sum(tags, [])
    tags = [tag.strip() for tag in tags]
    tagset = set(tags)
    tags = {tag: tags.count(tag) for tag in tagset}

    return render_template('index.html', posts=posts, tags=tags)


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


@home.route('/posts/tag-search/<string:tag>')
def tag_search(tag):
    posts = Post.query.filter_by(
        tags=tag, publish=True).order_by(Post.timestamp.desc()).all()

    return render_template('home_tag_search.html', posts=posts)
