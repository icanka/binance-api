"""SocketIO server for the trview web application.
"""
from flask import session, app, jsonify
from flask_socketio import SocketIO, emit


_socketio = SocketIO()


@_socketio.on("connect", namespace="/webhook")
def handle_connect():
    """Handle a client connection to the socketio server."""
    print("Client connected")
    session["socket_init"] = True
    emit("my_response", jsonify({"data": "Connected"}))


@_socketio.on("disconnect", namespace="/webhook")
def handle_disconnect():
    """Handle a client disconnection from the socketio server."""
    print("Client disconnected")
    session.pop("socket_init", None)
