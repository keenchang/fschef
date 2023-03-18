import os
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
socketio = SocketIO()


def create_app():
    app = Flask(__name__)

    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)

    db.init_app(app)
    socketio.init_app(app)

    # Register blueprints
    register_blueprints(app)

    return app


def register_blueprints(app):
    pass

