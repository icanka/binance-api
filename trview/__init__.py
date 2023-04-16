"""
trview package initializer.
CLI commands:
    flask --app trview populate-database --help
    flask --app trview init-db --help

"""

import os
from flask import Flask, request
from flask import make_response
from flask import redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from . import db
from . import webhook

# source set_up_environment.sh
# flask --app trview --debug run --host 0.0.0.0 --port 5000
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

    db.init_app(app)

    app.register_blueprint(webhook.bp)

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


# @app.route("/")
# def index():
#     return "<h1>Python Bot</h1>"


# @app.route("/make_response")
# def index2():
#     response = make_response("<h1>This document carries a cookie.</h1>")
#     response.set_cookie("answer", "42")
#     return response


# @app.route("/", methods=["POST"])
# def result():

#     return request.args.get("test-key")  # raw data
#     # json, if content-type of application/json is sent with the request
#     # pprint(request.json)
#     # json, if content-type of application/json is not sent
#     # pprint(request.get_json(force=True))


# @app.route("/user/<name>")
# def user(name):
#     return f"<h1>Hello, {name}</h1>"


# @app.route("/query-example")
# def query_example():
#     # If key doesn't exits, returns None
#     language = request.args.get("language")
#     test = request.args["test"]

#     return f"<h1>The language value is: {language} {test}</h1>"


# @app.route("/redirect/<redirect_address>")
# def rdirect(redirect_address):
#     return redirect(f"https://{redirect_address}")


# @app.route("/tradingview", methods=["POST"])
# def drsi_with_filters():
#     timestamp = time.time()
#     pprint(request.content_type)
#     pprint(request.json)
#     webhook_data = json.loads(request.data)
#     response = make_response()
#     response.status_code = 200
#     return response


# # app.run(debug=True, host='0.0.0.0', port=81)
