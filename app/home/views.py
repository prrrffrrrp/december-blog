from flask import Flask, render_template, url_for, redirect, session, flash

from . import home
from ..models import Post


@home.route('/')
def index():
    return render_template('index.html')


@home.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)
