from flask import Blueprint
from flask_cors import CORS

customers_bp = Blueprint('customers_bp', __name__, 
                         template_folder='templates', 
                         static_folder='static')

CORS(customers_bp, resources=r'/api/*')

from . import views
