from flask import Blueprint

stores_bp = Blueprint('stores_bp', __name__, template_folder='templates')

from . import views
