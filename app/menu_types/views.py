from . import menu_types_bp
from app.extensions import db
from app.models.stores import Store
from app.models.menu_types import Menu_type
from app.utils import check_login_in
from flask import render_template, redirect, url_for, request


@menu_types_bp.route('/store/<int:store_id>/menu_types')
@check_login_in()
def index(store_id):
    menu_types = Menu_type.query.filter_by(store_id=store_id).order_by(Menu_type.id).all()

    return render_template("menu_types/index.html", menu_types=menu_types, store_id=store_id)


@menu_types_bp.route('/store/<int:store_id>/menu_type/new')
@check_login_in()
def new(store_id):
    store = Store.query.get(store_id)

    return render_template("menu_types/new.html", store=store)


@menu_types_bp.route('/store/<int:store_id>/menu_type/create', methods=['POST'])
@check_login_in()
def create(store_id):
    store = Store.query.get(store_id)
    name = request.form['name']

    menu_type = Menu_type(name=name, store=store)
    db.session.add(menu_type)
    db.session.commit()

    return redirect(url_for('menu_types_bp.index', store_id=store_id))


@menu_types_bp.route('/menu_type/<int:id>/edit')
@check_login_in()
def edit(id):
    menu_type = Menu_type.query.get(id)

    return render_template('menu_types/edit.html', menu_type=menu_type)


@menu_types_bp.route('/menu_type/<int:id>/update', methods=['POST'])
@check_login_in()
def update(id):
    menu_type = Menu_type.query.get(id)

    menu_type.name = request.form['name']
    db.session.commit()

    return redirect(url_for('menu_types_bp.index', store_id=menu_type.store_id))


@menu_types_bp.route('/menu_type/<int:id>/delete')
@check_login_in()
def delete(id):
    menu_type = Menu_type.query.get(id)

    db.session.delete(menu_type)
    db.session.commit()

    return redirect(url_for('menu_types_bp.index', store_id=menu_type.store_id))
