from flask import Blueprint

menu_types_bp = Blueprint('menu_types_bp', __name__, 
                          template_folder='templates', 
                          static_folder='static')

from . import views
