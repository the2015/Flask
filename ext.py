import threading
import time
from threading import current_thread

import numpy as np
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask import json

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
lock = threading.Lock()

def init_ext(app):
    db.init_app(app=app)
    migrate.init_app(app, db)
    # DebugToolbarExtension(app)
    socketio.init_app(app)


# ndarray 转json
def ToJsonStr(arg):
    return json.dumps(arg.tolist())


# json转ndarray
def Tondarray(arg):
    return np.array(json.loads(arg), dtype=np.uint8)


def parse(future):
    print('%s' % (current_thread().name,))
