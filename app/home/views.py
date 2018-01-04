from flask import abort, render_template
from flask_login import current_user

from . import home
from ..models import Post, Tag


def clean_tags(data):
    tags = data.split(',')
    tags = [tag.strip() for tag in tags]
    return tags


@home.route('/')
def index():
    posts = Post.query.order_by(
        Post.timestamp.desc()).filter_by(publish=True).all()

    # This asks the database for tags and returns a list of tuples:
    # tags = Post.query.with_entities(Post.tags).all()

    tags = Tag.query.all()
    tags = [tag.tag_name for tag in tags]
    tags_set = set(tags)
    tags = {tag: tags.count(tag) for tag in tags_set}

    return render_template('index.html', posts=posts, tags=tags)


@home.route('/posts/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    tags = post.tags

    try:
        if post.publish or current_user.is_admin:
            return render_template('post.html', post=post, tags=tags)
        else:
            abort(403)
    except AttributeError:
        abort(403)


@home.route('/posts/tag-search/<string:tag>')
def tag_search(tag):
    tag_to_posts = Tag.query.filter_by(tag_name=tag).all()
    posts = []
    for tag in tag_to_posts:
        posts.append(tag.post)

    return render_template('home-tag-search.html', posts=posts)
