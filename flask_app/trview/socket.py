from flask import session, jsonify
from flask_socketio import emit
from .app_factory import _socketio


@_socketio.on("connect", namespace="/webhook")
def handle_connect():
    print("Client connected")
    session["socket_init"] = True
    emit("my_response", jsonify({"data": "Connected"}))
    

@_socketio.on("disconnect", namespace="/webhook")
def handle_disconnect():
    print("Client disconnected")
    session.pop("socket_init", None)
    
