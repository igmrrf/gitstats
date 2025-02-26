from flask.cli import with_appcontext
import click

from src.common.db import db


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    click.echo("Initialized the database.")
