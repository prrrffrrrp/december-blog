from flask import render_template, url_for, redirect, flash

from . import admin
from .. import db
from ..models import Post
from .forms import PostForm


@admin.route('/new-post', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    subtitle=form.subtitle.data,
                    tags=form.tags.data,
                    body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash('<{}> added to posts'.format(post.title))
        return redirect(url_for('home.index'))
    return render_template('new_post.html', form=form)
