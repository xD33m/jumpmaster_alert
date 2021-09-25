import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from DetectJumpmaster import detect_champion_selection, cancelAllTimers
from lib import utils
from lib import sockets
from threading import Thread, Event

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


@app.route("/start")
def start():
    print("Jumpmaster alert started\n")
    # https://stackoverflow.com/a/474543
    detect_champion_selection()

    return jsonify("App has startet")


@app.route("/stop")
def stop():
    print("Jumpmaster alert stopped\n")
    cancelAllTimers()

    return jsonify("App has stopped")


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


@socketio.on('message')
def handle_message(message):
    print('received message: ', message["status"])

    if (message["status"] == "Off"):
        cancelAllTimers()
        socketio.emit('status', {
            'data': 'Stopping Jumpmaster alert', 'status': 'Off'})
        socketio.emit('logs', "Jumpmaster alert stopped")

    elif (message["status"] == "On"):
        detect_champion_selection()
        socketio.emit('status', {
            'data': 'Starting Jumpmaster alert', 'status': 'On'})

    else:
        print("Unknown command")


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print('An error occured:')
    print(e)


if __name__ == "__main__":
    # app.run(**app_config)
    socketio.run(app, debug=True,
                 host=app_config["host"], port=int(app_config["port"]))
