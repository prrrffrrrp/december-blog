from flask import render_template, url_for, redirect, flash

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,)
        db.session.add(user)
        db.session.commit()
        flash('You have registered and may login')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Hello {}, your are logged in'.format(form.username.data))
        return redirect(url_for('home.index'))
    return render_template('login.html', form=form)
