import os
from app import create_app, db, clean_tags
from app.models import Post, Tag
from flask_migrate import Migrate

app = create_app(os.environ.get('APP_SETTINGS'))

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, clean_tags=clean_tags, db=db, Post=Post, Tag=Tag)
