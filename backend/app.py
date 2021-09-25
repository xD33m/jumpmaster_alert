from logging import debug
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from DetectJumpmaster import detect_champion_selection, cancelAllTimers
from lib import utils

app = Flask(__name__)
app_config = {"host": "0.0.0.0", "port": sys.argv[1], "debug": True}
app.config['PROPAGATE_EXCEPTIONS'] = True

utils.loadEnv()

"""
---------------------- DEVELOPER MODE CONFIG -----------------------
"""
# Developer mode uses app.py
if "app.py" in sys.argv[0]:
    # Update app config
    app_config["debug"] = True

    # CORS settings
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
# Quits Flask on Electron exit


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


if __name__ == "__main__":
    app.run(**app_config)
