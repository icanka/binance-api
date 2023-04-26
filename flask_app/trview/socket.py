"""SocketIO server for the trview web application.
"""
from time import sleep
from flask import request, session
from flask_socketio import SocketIO, emit
from .models import db, Webhooks
from pprint import pprint


_socketio = SocketIO()


@_socketio.on("connect")
def handle_connect(data):
    """Handle a client connection to the socketio server."""
    sleep(5)
    row_to_delete = db.session.query(Webhooks).first()
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

@_socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    emit('message', data, broadcast=True) # broadcast=True sends to all clients except the sender