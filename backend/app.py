
from threading import Thread, Event
from lib import sockets
from lib import alerts
from lib import utils
from DetectJumpmaster import detect_champion_selection, cancelAllTimers
from flask_cors import CORS
from flask import Flask, jsonify, request
import sys
from engineio.async_drivers import threading  # needed for pyinstaller
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler


app = Flask(__name__)
app_config = {"host": "0.0.0.0", "port": sys.argv[1]}

socketio = sockets.initSocketIO(app)
utils.loadEnv()

thread = Thread()
thread_stop_event = Event()

"""
---------------------- DEVELOPER MODE CONFIG -----------------------
"""
# Developer mode uses app.py
if "app.py" in sys.argv[0]:
    app_config["debug"] = True

    cors = CORS(
        app,
        resources={r"/*": {"origins": "http://localhost*"}},
    )

    # CORS headers
    app.config["CORS_HEADERS"] = "Content-Type"


"""
--------------------------- REST CALLS -----------------------------
"""


@app.route("/example")
def example():
    return jsonify("Example response from Flask! Learn more in /app.py & /src/components/App.js")


"""
-------------------------- APP SERVICES ----------------------------
"""


@app.route("/quit")
def quit():
    cancelAllTimers()
    shutdown = request.environ.get("werkzeug.server.shutdown")
    shutdown()


"""
-------------------------- WEBSOCKETS ----------------------------
"""

# Handle the webapp connecting to the websocket


@socketio.on('connect')
def connect():
    print('connected to websocket')


# Handle the webapp sending a message to the websocket


@socketio.on('toggle')
def handle_message(message):
    print('received message: ', message["status"])
    print('received message: ', message["type"])

    if (message["status"] == False):
        if(message["type"] == "startAndStop"):
            cancelAllTimers()
            socketio.emit('status', {
                'data': 'Stopping Jumpmaster alert', 'status': False})
            socketio.emit('logs', "Jumpmaster alert stopped")
            socketio.emit("detection_log", {
                "jumpDetection": False, "charDetection": False})
        if(message["type"] == "sound"):
            alerts.updateNotificationSettings(
                message["type"], message["status"])
            socketio.emit('logs', "Sound alert deactivated")
        if(message["type"] == "discordDM"):
            alerts.updateNotificationSettings(
                message["type"], message["status"])
            socketio.emit('logs', "Discord DM deactivated")

    elif (message["status"] == True):
        if(message["type"] == "startAndStop"):
            detect_champion_selection()
            socketio.emit('status', {
                'data': 'Starting Jumpmaster alert', 'status': True})
            socketio.emit("detection_log", {
                "jumpDetection": False, "charDetection": True})
        if(message["type"] == "sound"):
            alerts.updateNotificationSettings(
                message["type"], message["status"])
            socketio.emit('logs', "Sound alert activated")
        if(message["type"] == "discordDM"):
            alerts.updateNotificationSettings(
                message["type"], message["status"])
            socketio.emit('logs', "Discord DM activated")

    else:
        print("Unknown command")


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print('An error occured:')
    print(e)


def run_server():
    if app_config["debug"] is True:
        socketio.run(app, debug=True,
                     host=app_config["host"], port=int(app_config["port"]))
    else:
        server = WSGIServer(('0.0.0.0', int(app_config["port"])), app,
                            handler_class=WebSocketHandler)
        server.serve_forever()


if __name__ == "__main__":
    run_server()
