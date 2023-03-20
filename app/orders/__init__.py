from flask import Blueprint

orders_bp = Blueprint('orders_bp', __name__, template_folder='templates', static_folder='static')

from . import views
