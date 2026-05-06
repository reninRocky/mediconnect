from __future__ import annotations

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

# Threading mode is the most compatible default on Windows.
socketio = SocketIO(async_mode="threading")
bcrypt = Bcrypt()

