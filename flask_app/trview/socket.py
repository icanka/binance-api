"""SocketIO server for the trview web application.
"""
from time import sleep
from flask import request, session
from flask_socketio import SocketIO, Namespace, emit
from .models import db, Webhooks
from pprint import pprint


_socketio = SocketIO()


@_socketio.on("connect", namespace="/webhook_signal")
def handle_webhook_connect(json):
    """Handle a client connection to the socketio server."""
    print("Client connection webhooksignal acknowledged")


@_socketio.on("connect")
def handle_connect(data):
    """Handle a client connection to the socketio server."""
    connection_id = request.sid
    pprint(f"connection_id: {connection_id}")
    print("Client connection acknowledged")
    # row_to_delete = db.session.query(Webhooks).first()
    session["socket_init"] = True


@_socketio.on("client_connected")
def handle_client_connect():
    """Handle a client connection to the socketio server."""
    print("Client connection acknowledged")


@_socketio.on("disconnect")
def handle_disconnect():
    """Handle a client disconnection from the socketio server."""
    print("Client disconnected")
    session.pop("socket_init", None)


@_socketio.on("message")
def handle_message(data):
    """Handle a message from a client.

    Args:
        data (dict): Message data.
    """
    print("Received message:", data)
    emit(
        "message", data, broadcast=True
    )  # broadcast=True sends to all clients except the sender
