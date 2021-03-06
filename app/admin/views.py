from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .. import db, clean_tags
from ..models import Post, Tag
from .forms import PostForm


def check_admin():
    if not current_user.is_admin:
        abort(403)


@admin.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    check_admin()

    tag_search = False

    posts = Post.query.order_by(Post.timestamp.desc()).all()
    tags = Tag.query.all()
    tags = clean_tags(tags)
    tags = [tag for tag in set(tags)]
    tags.sort()

    return render_template('dashboard.html', posts=posts, tags=tags)


@admin.route('/admin/tag-search/<string:tag>')
@login_required
def tag_search(tag):
    check_admin()

    tag_search = True

    searched_tags = Tag.query.filter(Tag.tag_name.contains(tag)).all()
    posts = [tag.post for tag in searched_tags]
    tags = Tag.query.all()
    tags = clean_tags(tags)
    tags = [tag for tag in set(tags)]

    return render_template('admin-tag-search.html', posts=posts, tag=tag, tags=tags)


@admin.route('/admin/posts/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    check_admin()

    add_post = True

    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data)
        tags = Tag(tag_name=form.tags.data, post=post)

        db.session.add(post)
        db.session.add(tags)
        db.session.commit()

        flash('{} added to posts'.format(post.title))

        return redirect(url_for('admin.dashboard'))

    return render_template('add-edit-post.html', action="Add",
                           add_post=add_post, form=form)


@admin.route('/admin/posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    check_admin()

    add_post = False

    post = Post.query.get_or_404(id)
    tags = Tag.query.filter_by(post_id=id).first()

    form = PostForm(data={'title': post.title,
                          'tags': tags.tag_name,
                          'body': post.body})

    if form.validate_on_submit():
        post.title = form.title.data
        tags.tag_name = form.tags.data
        post.body = form.body.data

        db.session.add(post)
        db.session.add(tags)

        db.session.commit()

        flash('You have edited post: {}'.format(post.title))

        return redirect(url_for('admin.dashboard'))

    return render_template('add-edit-post.html', action="Edit",
                           add_post=add_post, form=form)


@admin.route('/admin/posts/<int:id>/publish', methods=['GET', 'POST'])
@login_required
def publish_post(id):
    check_admin()

    post = Post.query.get_or_404(id)
    if not post.publish:
        post.publish = True

        flash("You have published post: {}".format(post.title))
    else:
        post.publish = False

        flash("The post: {}, isn't public no more".format(post.title))

    db.session.add(post)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

    return render_template()


@admin.route('/admin/posts/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    check_admin()

    post = Post.query.get_or_404(id)
    tags = Tag.query.filter_by(post_id=id).first()
    db.session.delete(post)
    if tags:
        db.session.delete(tags)
    db.session.commit()
    flash('You have deleted post: {}'.format(post.title))

    return redirect(url_for('admin.dashboard'))

    return render_template(title='Delete Post')
