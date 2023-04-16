"""Database module, including the SQLAlchemy database object and DB-related utilities."""

import sqlite3
import importlib
import inspect
import sys
import click
from flask import current_app
from flask import g
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import SQLAlchemyError
from trview.models import db, populate_database


# Deprecated with sqlalchemy use db instance instead.
def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# Deprecated with sqlalchemy use db instance instead
def close_db(e=None):
    """If this request connected to the database, close the connection."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(create=False, fresh=False):
    """Clear existing data and create new tables. Create the database if it does not exist."""
    try:
        if fresh and database_exists(db.engine.url):
            click.echo("Dropping all tables.")
            db.drop_all()
        if create and not database_exists(db.engine.url):
            click.echo(f"Creating database: {db.engine.url}")
            create_database(db.engine.url)

        click.echo("Initialized database.")
        db.create_all()  # this seems to create the database too if it does not exist.
    except SQLAlchemyError as exc:
        click.echo(f"An error occurred while initializing the database: {exc}")


@click.command("init-db")
@click.option("--create", help="Create the database if not exists.", is_flag=True)
@click.option(
    "--fresh", help="Drop all tables and create a fresh database.", is_flag=True
)
def init_db_command(create, fresh):
    """Clear existing data and create new tables."""
    init_db(create, fresh)


def init_app(app):
    """Register the database functions with the Flask app. This is called by the
    application factory.
    Setup Flask application that uses SQLAlchemy to interact with a SQLite database.
    """
    # app.teardown_appcontext(close_db)  this is not needed with sqlalchemy
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_database)
    app.cli.add_command(test)

    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = current_app.config["DATABASE"]
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)


@click.command("test")
def test():
    print("test")
    call_model_function("insert_user", "trview.models", "test", "test", "test", "test")


def call_model_function(function_name, *args, model="trview.models", **kwargs):
    """
    Call a function on a model. Do not use method from the model class directly from blueprints.
    This method is used to call a function on a model class for encapsulation.
    """
    model_classes = [
        obj
        for name, obj in inspect.getmembers(sys.modules[model], inspect.isclass)
        if obj.__module__ == model
    ]

    for model_class in model_classes:
        for name, obj in inspect.getmembers(model_class, inspect.isfunction):
            if name == function_name:
                return getattr(model_class, function_name)(*args, **kwargs)
