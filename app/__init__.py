import os
from flask import Flask
from app.extensions import db, socketio
from app.models import users, stores, menu_types, tables, orders


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
    from app.stores import stores_bp
    app.register_blueprint(stores_bp)

    from app.users import users_bp
    app.register_blueprint(users_bp)

    from app.menu_types import menu_types_bp
    app.register_blueprint(menu_types_bp)

    from app.menus import menus_bp
    app.register_blueprint(menus_bp)

    from app.tables import tables_bp
    app.register_blueprint(tables_bp)

    from app.customers import customers_bp
    app.register_blueprint(customers_bp)

