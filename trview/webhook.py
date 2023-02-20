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

bp = Blueprint("webhook", __name__, url_prefix="/webhook")


@bp.route("/drsi_with_filters", methods=["POST"])
def drsi_with_filters():
    """save the posted json to database"""
    # timestamp = time.time()
    db = get_db()
    pprint(request.content_type)
    pprint(request.json)
    rd = json.loads(request.data)
    response = make_response()
    try:
        test = db.execute(
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

        # db.commit()

    except db.Error:
        response = make_response("<h1>Database Error</h1>")

    response.status_code = 200
    return response


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("webhook.login"))

        flash(error)

    return render_template("webhook/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
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

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("webhook/login.html")


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
