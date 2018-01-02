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

#     tags = [clean_tags(post.tags) for post in posts]
#     tags = sum(tags, [])
#     tagset = set(tags)
#     tags = {tag: tags.count(tag) for tag in tagset}

    tag_query = Tag.query.all()
    tags = [t.tags for t in tag_query]

    return render_template('index.html', posts=posts, tags=tags)


@home.route('/posts/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    tag_data = Tag.query.filter_by(post_id=post.id)

    tags = [t.tags for t in tag_data]

    try:
        if post.publish or current_user.is_admin:
            return render_template('post.html', post=post, tags=tags)
        else:
            abort(403)
    except AttributeError:
        abort(403)


@home.route('/posts/tag-search/<string:tag>')
def tag_search(tag):
    posts = Post.query.filter(
        Post.tags.contains(tag)).filter_by(
            publish=True).order_by(Post.timestamp.desc()).all()

    return render_template('home-tag-search.html', posts=posts)
