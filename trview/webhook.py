"""Webhook views"""

import functools
import json
import hashlib
import re
from pprint import pprint
from werkzeug.security import check_password_hash
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    make_response,
    jsonify,
)
from trview.models import db, Users, Webhooks
from trview.db import get_db, _db, get_class


bp = Blueprint("webhook", __name__, url_prefix="/webhook", static_folder="AdminLTE")


# @bp.route("/signals")
# def signals():
#     return render_template("webhook/content.html")
@bp.route("/database")
def database():
    """Render the database page.

    Returns:
        str: The rendered page.
    """

    result = db.session.query(Users).all()
    return result


def login_required(view):
    """Redirect user to login page if not already logged in"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("webhook.loginv2"))

        return view(**kwargs)

    return wrapped_view


@bp.route("/")
@login_required
def index():
    """Show the index page"""
    return render_template("webhook/index.html")


@bp.route("/pages/<page>", methods=["POST", "GET"])
@login_required
def pages(page):
    """Render the pages and return the partial content if it is an AJAX request or the full page if it is not.
    Args:
        page (str): The page to be rendered.
    Returns:
        str: The rendered page.
    """
    print("pages endpoint")
    if request.method == "POST":
        print("This is a POST request.")
        href_value = request.form["href"]
    elif request.method == "GET":
        # User refreshed the page.
        print("this is a GET request.")
        href_value = page
    print(href_value)
    # Check if the request is an AJAX request
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # If it is return only the partial content.
        print("ajax request.")
        return render_template(f"{href_value}.html")
    else:
        print("Not an ajax request.")
        return render_template(
            "webhook/base.html",
            content=render_template(f"webhook/pages/{href_value}.html"),
        )


@bp.route("/pages/signals", methods=["POST", "GET"])
@login_required
def signals():
    """Render the signals page and return the partial content if it is an AJAX request or the full page if it is not.
    Returns:
        str: The rendered page.
    """
    # Check if the request is an AJAX request
    signal_data = db.session.query(Webhooks).all()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # If it is return only the partial content.
        print("ajax request.")
        return render_template("webhook/pages/signals.html")
    else:
        print("Not an ajax request.")
        return render_template(
            "webhook/base.html",
            content=render_template("webhook/pages/signals.html"),
        )


@bp.route("/api/data/<table>", methods=["POST", "GET"])
# @login_required
def data(table):

    """
    Get the data from the database and return it as a json object.
    Args:
        table (str): The table model to get the data from.

    Returns:
        dict: The data from the database.
    """

    def searchable_columns():
        columns = 0
        for key in request.args.keys():
            if "columns" in key and "data" in key:
                columns += 1
        searchable_columns = [
            request.args.get(f"columns[{i}][data]", type=str)
            for i in range(columns)
            if request.args.get(f"columns[{i}][searchable]", type=bool)
        ]
        return searchable_columns

    table = get_class(table.capitalize())
    query = table.query
    search = request.args.get("search[value]", type=str)
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    try:
        if search:
            or_clauses = [
                table.__table__.columns[column].like(f"%{search}%")
                for column in searchable_columns()
            ]
            query = query.filter(db.or_(*or_clauses))
        total_filtered = query.count()
        query = query.offset(start).limit(length)
    except AttributeError:
        return jsonify({"error": "Not Found."}), 404

    return jsonify(
        {
            "data": [table_data.to_dict() for table_data in query],
            "recordsFiltered": total_filtered,
            "recordsTotal": table.query.count(),
            "draw": request.args.get("draw", type=int),
        }
    )


# TODO: refactor this function according to the new database structure.
@bp.route("/drsi_with_filters", methods=["POST"])
def drsi_with_filters():
    """
    Save the posted json to database

    This endpoint is intended for tradingview. Expected example json with key:value format;

    {
    "strategy_name" : "drsi_with_filters",
    "action": "buy",
    "alert_message": "",
    "contracts": "0.019893",
    "market_position": "long",
    "market_position_size": "0.009942",
    "order_id": "long",
    "position_size": "0.009942",
    "price": "23027.08",
    "ticker": "BTCBUSD"
    }
    """
    db = get_db()
    pprint(request.content_type)
    pprint(request.json)
    rd = json.loads(request.data)
    # create an empty response object
    response = make_response()
    # insert the json to sqlite database
    try:
        db.execute(
            """
            INSERT INTO webhooks (
                strategy_name,
                ticker,
                strategy_action,
                market_position,
                price,
                position_size,
                market_position_size,
                contracts,
                order_id
            ) VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                rd["strategy_name"],
                rd["ticker"],
                rd["action"],
                rd["market_position"],
                rd["price"],
                rd["position_size"],
                rd["market_position_size"],
                rd["contracts"],
                rd["order_id"],
            ),
        )
        # data is only data if you're committed enough.
        db.commit()

    # ooopps
    except db.Error:
        # create some generick error response.
        response = make_response("<h1>Database Error</h1>")

    response.status_code = 200
    return response


@bp.route("/register", methods=("GET", "POST"))
def register():  # TODO review this function
    """Render the register page and register the user if the form is submitted."""
    # someone is trying to register
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # basic sanity check although we expect it to be dealt with in front-end.
        if not username or not password:
            flash("Username and password are required.")
        else:
            _db("insert_user", username, password)
            return redirect(url_for("webhook.loginv2"))
        # flash the error data so it can be used in template to inform user

    return render_template("webhook/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Render the login page and login the user if the form is submitted.

    Returns:
        str: The rendered page.
    """
    # somone is trying to login
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        # Does the user really exist? or its just an idea? if it is can we kill him?
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        # don't tell the user what was wrong exactly.
        if user is None or not check_password_hash(user["password"], password):
            error = "Incorrect username or password."

        if error is None:
            session.clear()
            salt = app.config["SECRET_KEY"]
            # Concatenate the user id with the salt
            data_with_salt = user["id"] + salt
            # Hash the data with md5
            md5_hashed_session = hashlib.md5(data_with_salt).hexdigest()
            session["session_id"] = md5_hashed_session
            return redirect(url_for("index"))

        flash(error)

    return render_template("webhook/login.html")


@bp.route("/loginv2", methods=("GET", "POST"))
def loginv2():
    print("LOGINV2")
    if request.method == "POST":
        user_id = session.get("user_id")

        if user_id is not None:
            print("Redirecting to index")
            return redirect(url_for("webhook.index"))

        username = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None or not check_password_hash(user["password"], password):
            error = "Incorrect username or password."

        # successful login
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("webhook.index"))

        flash(error)

    return render_template("webhook/login-v2.html")


@bp.route("/validate_user", methods=["POST"])
def validate_user():
    """This method is for for validating user
    used primarily in javascript for interactive user validating.

    Returns:
        Response: The response object indicating the state of the validation.
    """

    print("VALIDATE ENDPOINT")
    print(db)
    # rd = json.loads(request.data)
    rd = request.get_json()
    response = make_response()
    username = rd["email"]
    password = rd["password"]
    print(f"pass:'{password}'")
    # db = get_db()
    error = None
    print(username)
    user = db.session.query(Users).filter_by(username=username).first()
    if user is not None:
        print(user.username)
        print(f"pass:'{user.password}'")
        print(check_password_hash(user.password, password))
    else:
        print("User is None")
    print("chekcing user credentials")

    # return response
    # user = db.execute("SELECT * from user WHERE username = ?", (username,)).fetchone()
    # print(rd)
    # past= check_password_hash(user["password"], password)
    # print(f"user: {past}")

    if user is not None and check_password_hash(user.password, password):
        print("TRUE")
        session.clear()
        session["user_id"] = user.id
        response.status_code = 200
        response.data = "Login Succesfull"
        print(response.status)
        return response
        # return render_template(url_for("index"))
    else:
        print("FALSE")
        # return a message with unathorized access code.
        response = make_response("Incorrect credentials", 401)
        return response


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(Users).filter_by(id=user_id).first()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
