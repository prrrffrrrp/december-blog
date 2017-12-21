from flask import render_template, url_for, redirect, flash

from . import auth
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Hello {}, your are logged in'.format(form.username.data))
        return redirect(url_for('home.index'))
    return render_template('login.html', form=form)
