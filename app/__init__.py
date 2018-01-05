from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown

db = SQLAlchemy()
login_manager = LoginManager()
pagedown = PageDown()


def clean_tags(tag_query):
    tags = [t.tag_name for t in tag_query]
    tags = [t.split(',') for t in tags]
    tags = sum(tags, [])
    tags = [t.strip() for t in tags]
    return tags


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    Bootstrap(app)
    db.init_app(app)
    pagedown.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "home.index"

    migrate = Migrate(app, db)

    from app import models

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html'), 500

    return app
