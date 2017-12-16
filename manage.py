import os
from app.app import app, db
from app.models import Post
from flask_migrate import Migrate

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Post=Post)
