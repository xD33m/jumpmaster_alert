from flask_socketio import SocketIO, emit

lastDetection = None


def initSocketIO(app):
    global socketio
    socketio = SocketIO(app, cors_allowed_origins="*")
    return socketio


def getSocketIO():
    return socketio


def emitEvent(event, message):
    socketio.emit(event, message)
    print(event, message)


def emitDetectionEvent(jumpmasterDetection=False, championDetection=False):
    global lastDetection
    currentDetection = 'champion' if championDetection else 'jumpmaster'
    # if last detection matches current detection, do nothing
    if jumpmasterDetection is True and currentDetection != lastDetection:
        emitEvent("detection_log",
                  {"message": "Looking for jumpmaster...", "type": "jumpmaster", "loading": True})
        lastDetection = currentDetection

    if championDetection is True and currentDetection != lastDetection:
        emitEvent("detection_log",
                  {"message": "Looking for champion selection...", "type": "champion", "loading": True})
        lastDetection = currentDetection


def resetDetection():
    global lastDetection
    lastDetection = None
