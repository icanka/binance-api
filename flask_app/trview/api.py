""" api for trview
"""

import json
import time
from flask import (
    Blueprint,
    request,
    session,
    make_response,
    Response,
    jsonify,
)
from flask_socketio import emit
from .db import get_class
from pprint import pprint

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/websocket")
def websocket():
    """Return the websocket URL."""
    return "ws://localhost:5000/webhook"


@bp.route("/database_get_all/<table>", methods=["GET"])
def database(table):
    """Get all Users"""
    result = db.session.query(table).all()
    return result


@bp.route("/test")
def some_endpoint():
    # Extract the value of 'var1' from the query string
    var1 = request.args.get("var1")
    # Do something with var1
    return "Received var1 value: {}".format(var1)


@bp.route("/database/<table_name>", methods=["GET"])
def _database(table_name):
    """Get column names from the database."""
    table = get_class(table_name.capitalize())
    column_names = table.__table__.columns.keys()
    return jsonify(column_names)


@bp.route("/delete", methods=["POST"])
def delete():
    """Delete the first row from the database and emit an event to the c
    lient to update the table."""
    table_name = request.args.get("table_name")
    clazz = get_class(table_name.capitalize())
    print(clazz)
    print(type(clazz))
    row_to_delete = db.session.query(clazz).first()
    db.session.delete(row_to_delete)
    db.session.commit()
    emit("update_table", broadcast=True, namespace="/webhook_signal")
    return make_response(jsonify({"message": "Deleted"}), 200)


# TODO: refactor this function according to the new database structure.


@bp.route("/drsi_with_filters", methods=["POST"])
def drsi_with_filters():
    """
    Save the posted json to database

    This endpoint is intended for tradingview.
    Expected example json with key:value format;

    {
    "strategy_name" : "drsi_with_filters",
    "alert_message":"{{strategy.order.alert_message}}",
    "action": "{{strategy.order.action}}",
    "contracts": "{{strategy.order.contracts}}",
    "market_position": "{{strategy.market_position}}",
    "market_position_size": "{{strategy.market_position_size}}",
    "order_id": "{{strategy.order.id}}",
    "price": "{{strategy.order.price}}",
    "ticker": "{{ticker}}",
    "firetime" : "{{timenow}}",
    "interval" : "{{interval}}"
    }


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
    pprint("drsi_with_filter endpint")
    rd = json.loads(request.data)
    curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    pprint("-----------------------------------------------------------------")
    pprint(f"--------------------------{curtime}-----------------------------")
    pprint(rd)
    pprint(request.content_type)
    pprint(request.headers)
    pprint("-----------------------------------------------------------------")
    # create an empty response object
    response = make_response()
    # insert the json to sqlite database
    # try:
    #     db.execute(
    #         """
    #         INSERT INTO webhooks (
    #             strategy_name,
    #             ticker,
    #             strategy_action,
    #             market_position,
    #             price,
    #             position_size,
    #             market_position_size,
    #             contracts,
    #             order_id
    #         ) VALUES (?,?,?,?,?,?,?,?,?)""",
    #         (
    #             rd["strategy_name"],
    #             rd["ticker"],
    #             rd["action"],
    #             rd["market_position"],
    #             rd["price"],
    #             rd["position_size"],
    #             rd["market_position_size"],
    #             rd["contracts"],
    #             rd["order_id"],
    #         ),
    #     )
    #     # data is only data if you're committed enough.
    #     db.commit()

    # # ooopps
    # except db.Error:
    #     # create some generick error response.
    #     response = make_response("<h1>Database Error</h1>")

    response.status_code = 200
    return response
