import functools
import time
import json
from pprint import pprint
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
)
from werkzeug.security import check_password_hash, generate_password_hash
from trview.db import get_db

bp = Blueprint("webhook", __name__, url_prefix="/webhook", static_folder="AdminLTE")


@bp.route("/drsi_with_filters", methods=["POST"])
def drsi_with_filters():
    """
    Save the posted json to database

    This endpoint is intented for tradingview. Expected example json with key:value format;

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
    # timestamp = time.time()
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
def register():
    # someone is trying to register
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        # basic sanity check altohugh we expect it to be dealt with in front-end.
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                # only insert the password hash to the database
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                # redirect user to the login page after successfull login
                return redirect(url_for("webhook.login"))
        # flash the error data so it can be used in template to inform user
        flash(error)

    return render_template("webhook/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
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
        if user is None:
            error = "Incorrect username or password."
        # even we don't know the users password, coool.
        elif not check_password_hash(user["password"], password):
            error = "Incorrect username or password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("webhook/login.html")


@bp.route("/loginv2", methods=("GET", "POST"))
def loginv2():
    print("LOGINV2")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username or password."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect username or password."

        # successful login
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("webhook/login-v2.html")


@bp.route("/validate_user", methods=["POST"])
def validate_user():
    """This method is for for validating user
    used primarily in javascript for interactive user validating.

    Returns:
        Response: The response object indicating the state of the validation.
    """
    # rd = json.loads(request.data)
    rd = request.get_json()
    response = make_response()
    username = rd["email"]
    password = rd["password"]
    db = get_db()
    error = None
    user = db.execute("SELECT * from user WHERE username = ?", (username,)).fetchone()
    print("chekcing user credentials")
    print(rd)
    #past= check_password_hash(user["password"], password)
    #print(f"user: {past}")
    if user is not None and check_password_hash(user["password"], password):
        print("TRUE")
        session.clear()
        session["user_id"] = user["id"]
        response.status_code = 200
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
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("webhook.login"))

        return view(**kwargs)

    return wrapped_view
