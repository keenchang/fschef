from flask import Blueprint

tables_bp = Blueprint('tables_bp', __name__, template_folder='templates', static_folder='static')

from . import views
