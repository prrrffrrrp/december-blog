from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .. import db
from ..models import Post
from .forms import PostForm


def check_admin():
    if not current_user.is_admin:
        abort(403)


@admin.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    check_admin()

    posts = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template('dashboard.html', posts=posts)


@admin.route('/admin/posts/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    check_admin()

    add_post = True

    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    subtitle=form.subtitle.data,
                    tags=form.tags.data,
                    body=form.body.data)

        db.session.add(post)
        db.session.commit()

        flash('<{}> added to posts'.format(post.title))

        return redirect(url_for('admin.dashboard'))

    return render_template('add-edit-post.html', action="Add",
                           add_post=add_post, form=form)


@admin.route('/admin/posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    check_admin()

    add_post = False

    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.tags = form.tags.data
        post.body = form.body.data

        db.session.add(post)
        db.session.commit()

        flash('You have edited the post')

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

        flash("You have published the post")
    else:
        post.publish = False

        flash("The post isn't public no more")

    db.session.add(post)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

    return render_template()


@admin.route('/admin/posts/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    check_admin()

    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('You have deleted the post')

    return redirect(url_for('admin.dashboard'))

    return render_template(title='Delete Post')
