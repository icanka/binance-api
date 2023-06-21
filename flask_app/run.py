"""Run the flask with socketio server.
"""
from trview.app import create_app
from trview.socket import _socketio


if __name__ == "__main__":
    app = create_app()
    _socketio.init_app(app)
    # print app configuration
    _socketio.run(app)
