from flask import abort, render_template
from flask_login import current_user

from . import home
from ..models import Post, Tag
from .. import clean_tags


@home.route('/')
def index():
    posts = Post.query.order_by(
        Post.timestamp.desc()).filter_by(publish=True).all()

    # This asks the database for tags and returns a list of tuples:
    # tags = Post.query.with_entities(Post.tags).all()

    tags = [post.tags for post in posts]
    tags = sum(tags, [])
    tags = clean_tags(tags)
    tags_set = set(tags)
    tags = {tag: tags.count(tag) for tag in tags_set}

    return render_template('index.html', posts=posts, tags=tags)


@home.route('/posts/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    tags = post.tags
    tags = clean_tags(tags)

    try:
        if post.publish or current_user.is_admin:
            return render_template('post.html', post=post, tags=tags)
        else:
            abort(403)
    except AttributeError:
        abort(403)


@home.route('/posts/tag-search/<string:tag>')
def tag_search(tag):
    tag_to_posts = Tag.query.filter(Tag.tag_name.contains(tag)).all()
    posts = [t.post for t in tag_to_posts]

    return render_template('home-tag-search.html', posts=posts)
