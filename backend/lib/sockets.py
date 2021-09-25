from flask_socketio import SocketIO, emit


def initSocketIO(app):
    global socketio
    socketio = SocketIO(app, cors_allowed_origins="*")
    return socketio


def getSocketIO():
    return socketio


def emitEvent(event, message):
    socketio.emit(event, message)
    print(event, message)
