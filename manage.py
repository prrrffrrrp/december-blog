import os
from app import create_app, db
from app.models import Post
from flask_migrate import Migrate

app = create_app(os.getenv('APP_SETTINGS'))

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Post=Post)
