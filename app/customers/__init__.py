from flask import Blueprint

customers_bp = Blueprint('customers_bp', __name__, 
                         template_folder='templates', 
                         static_folder='static')

from . import views
