"""
trview package initializer.
CLI commands:
    source set_up_environment.sh for the environment variables to be set.
    flask --app trview populate-database --help
    flask --app trview init-db --help
    flask --app trview --debug run --host 0.0.0.0 --port 5000

"""


import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from . import db
from . import webhook


def create_app(test_config=None):
    """Create and configure an instance of the Flask application.
    This is factory function that creates the Flask app and configures it."""

    app = Flask(__name__, instance_relative_config=True)
    # Set some default initial configuration that the app will use
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        APPLICATION_NAME="Trview",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "trading.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # overrides the default configuration with values taken from config.py
        environment_configuration = os.environ["CONFIGURATION_SETUP"]
        app.config.from_object(environment_configuration)
        # app.config.from_pyfile("config.py", silent=True)
    else:
        # load test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands

    app.register_blueprint(webhook.bp)
    db.init_app(app)
    limiter = Limiter(
        get_remote_address,
        app=app,
        storage_uri="memory://",
    )

    # limit the number of requests per second and minute
    limiter.limit("50/second")(webhook.bp)
    limiter.limit("500/minute")(webhook.bp)

    # limiter.init_app(app)
    # print(app.__name__)
    # limiter.limit('3/second')(app)
    return app
