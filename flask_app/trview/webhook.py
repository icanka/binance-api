"""Webhook views"""

import functools
from itertools import count
import hashlib
import time
from pprint import pprint
from werkzeug.security import check_password_hash
from flask import (
    current_app,
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    make_response,
    Response,
    jsonify,
)

from .models import db, Users
from .db import get_db, _db, get_class

bp = Blueprint("webhook", __name__, url_prefix="/webhook",
               static_folder="AdminLTE")


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
    """
    Render the pages and return the partial content if it is an AJAX request.
    Args:
        page (str): The page to be rendered.
    Returns:
        str: The rendered page.
    """
    print("/pages endpoint")
    if request.method == "POST":
        href_value = request.form["href"]
        print("POST REUQEST")

    elif request.method == "GET":  # 'GET' is deprecated
        # User refreshed the page or navigated to the page.
        print("GET REQUEST")
        href_value = page

    # Check if the request is an AJAX request
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # If it is return only the partial content.
        print("AJAX REQUEST, RETURNING PARTIAL CONTENT")
        return render_template(f"{href_value}.html")

    else:
        return render_template(
            "webhook/base.html",
            content=render_template(f"webhook/pages/{href_value}.html"),
        )


@bp.route("/pages/signals", methods=["POST", "GET"])
@login_required
def database():
    """
    Render the signals page and return the partial content if it is an 
    AJAX request or the full page if it is not.
    Returns:
        str: The rendered page.
    """
    # Check if the request is an AJAX request
    # signal_data = db.session.query(Webhooks).all()
    tables = db.metadata.tables.keys()
    table_name = None
    print("SIGNALS")
    if (request.args.get('table') is None):
        table_name = 'Webhooks'
    else:
        table_name = request.args.get('table')

    print(f"table: {request.args.get('table')}")
    print(f"table_name: {table_name}")
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # If it is return only the partial content.
        pprint(f"request.args: {request.args}")
        table = get_class(table_name.capitalize())
        columns = table.__table__.columns.keys()
        return render_template("webhook/pages/signals.html", table_name=table_name,
                               columns=columns, tables=tables)
    else:
        table = get_class(table_name.capitalize())
        columns = table.__table__.columns.keys()
        return render_template(
            "webhook/base.html",
            content=render_template(
                "webhook/pages/signals.html", table_name=table_name,
                columns=columns, tables=tables),
        )


@bp.route("/api/data/<table>", methods=["POST", "GET"])
# @login_required
def data(table):
    """
    Get the data from the database and return it as a json object.
    Only searches the columns that are configured as searchable.
    Args:
        table (str): The table model to get the data from.

    Returns:
        dict: The data from the database.
    """
    start_time = time.time()

    table = get_class(table.capitalize())
    query = table.query
    order = get_order_columns(table)

    if order:
        query = query.order_by(*order)

    search = request.args.get("search[value]", type=str)
    pprint(f"request.args: {request.args}")
    try:
        total_filtered, query = apply_search_filter(query, search, table)
        start, length = get_pagination_parameters()
        query = query.offset(start).limit(length)

    except AttributeError:
        return jsonify({"error": "Not Found."}), 404

    response_data = {
        "data": [table_data.to_dict() for table_data in query],
        "recordsFiltered": total_filtered,
        "recordsTotal": table.query.count(),
        # This is the draw counter that DataTables is expecting to be returned from the server.
        "draw": request.args.get("draw", type=int),
    }

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time}")
    return jsonify(response_data)


@bp.route("/api/export", methods=["GET"])
# @login_required
def export():
    """Datatables export function.
    Export the data from the database as a csv file.
    Args:
        table (str): The table model to get the data from.

    Returns:
        str: The csv file.
    """
    file_format = request.args.get("format", type=str)
    table = request.args.get("table_name", type=str)
    if file_format == "csv":
        table = get_class(table.capitalize())
        table_data = table.query.all()
        csv = (
            ",".join([column.name for column in table.__table__.columns])
            + "\n"
            + "\n".join(
                [
                    ",".join(
                        [
                            str(getattr(row, column.name))
                            for column in table.__table__.columns
                        ]
                    )
                    for row in table_data
                ]
            )
        )

    # return the csv file
    response = Response(csv, mimetype="text/csv")
    response.headers.set("Content-Disposition",
                         "attachment", filename=f"{table}.csv")
    return response


@bp.route("/register", methods=("GET", "POST"))
def register():  # TODO review this function
    """Render the register page and register the user if the form is submitted.
    Some basic sanity checks are done here but it is expected to be dealt with in front-end.
    """
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


# Deprecated
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
            salt = current_app.config["SECRET_KEY"]
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
    """Render the login page and login the user if the form is submitted.

    Returns:
        str: The rendered page.
    """
    if request.method == "POST":
        user_id = session.get("user_id")

        if user_id is not None:
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
    """This method is for validating user
    used primarily in javascript for interactive user validating.
    Returned responses's text is used in javascript to inform user about 
    the state of the validation.

    Returns:
        Response: The response object indicating the state of the validation.
    """

    response_data = request.get_json()
    response = make_response()
    username = response_data["email"]
    password = response_data["password"]
    user = db.session.query(Users).filter_by(username=username).first()
    if user is not None:
        print(check_password_hash(user.password, password))
    else:
        print("User is None")

    if user is not None and check_password_hash(user.password, password):
        session.clear()
        session["user_id"] = user.id
        response.status_code = 200
        response.data = "Login Successful"
        return response
    else:
        # return a message with unauthorized access code.
        response = make_response("Incorrect credentials", 401)
        return response


@bp.before_app_request
def load_logged_in_user():
    """Load the user object from the database if a user is logged in."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(Users).filter_by(id=user_id).first()


@bp.route("/logout")
def logout():
    """Log out the current user and redirect to the index page.

    Returns:
        str: The rendered page.
    """
    session.clear()
    return redirect(url_for("index"))


def get_order_columns(table) -> list:
    """Get the columns to order by from the request.

    Args:
        table (_type_): The table to order by.

    Returns:
        list: List of columns to order by.
    """
    
    order_columns = []
    for i in count():
        col_index = request.args.get(f"order[{i}][column]", type=int)
        if col_index is None:
            break
        col_name = request.args.get(f"columns[{col_index}][data]", type=str)
        if is_column_orderable(col_name):
            descending = request.args.get(
                f"order[{i}][dir]", type=str) == "desc"
            col = getattr(table, col_name)
            col = col.desc() if descending else col.asc()
            order_columns.append(col)
    return order_columns


def apply_search_filter(query, search, table) -> tuple:
    """Apply the search filter to the query."""
    if search:
        or_clauses = [
            table.__table__.columns[column].like(f"{search}%")
            for column in searchable_columns()
        ]
        query = query.filter(db.or_(*or_clauses))

    total_filtered = query.count()
    return total_filtered, query


def searchable_columns() -> list:
    """Get the columns that are searchable by from the request."""
    columns = get_table_columns()
    searchable_cols = [
        request.args.get(f"columns[{i}][data]", type=str)
        for i in range(columns)
        if request.args.get(f"columns[{i}][searchable]", type=str) == "true"
    ]
    return searchable_cols


def orderable_columns() -> list:
    """Get the columns that are orderable by from the request."""
    columns = get_table_columns()
    for key in request.args.keys():
        if "columns" in key and "data" in key:
            columns += 1
    orderable_cols = [
        request.args.get(f"columns[{i}][data]", type=str)
        for i in range(columns)
        if request.args.get(f"columns[{i}][orderable]", type=str) == "true"
    ]
    return orderable_cols


def get_table_columns() -> int:
    """Get the number of columns in the table from the request."""
    columns = 0
    for key in request.args.keys():
        if "columns" in key and "data" in key:
            columns += 1
    return columns


def get_pagination_parameters() -> tuple:
    """Get the pagination parameters from the request."""
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    return start, length


def is_column_orderable(column_name) -> bool:
    """Check if the column is orderable."""
    return column_name in searchable_columns()


def is_column_searchable(column_name) -> bool:
    """Check if the column is searchable."""
    return column_name in searchable_columns()
