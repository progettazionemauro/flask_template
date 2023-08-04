import click
from flask.cli import with_appcontext
from app import app, db
from user_models import UserRegistration

@app.cli.command()
@with_appcontext
def init_users_db():
    """Initialize the users.db database."""
    with app.app_context():
        db.create_all(bind='users')
    click.echo('User registration database initialized.')
