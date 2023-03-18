from . import stores_bp
from flask import render_template


@stores_bp.route('/stores')
def index():
    return render_template('stores/index.html')
