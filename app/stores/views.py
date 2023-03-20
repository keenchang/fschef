from . import stores_bp
from app.extensions import db
from app.models.users import User
from app.models.stores import Store
from app.utils import check_login_in
from flask import render_template, redirect, url_for, request, session


@stores_bp.route('/stores')
@check_login_in()
def index():
    user_id = session.get("id")

    user = User.query.filter_by(id=user_id).first()
    stores = Store.query.filter_by(user_id=user_id).order_by(Store.id).all()

    return render_template("stores/index.html", user=user, stores=stores)


@stores_bp.route('/store/new')
@check_login_in()
def new():
    return render_template("stores/new.html")


@stores_bp.route('/store/create', methods=['POST'])
@check_login_in()
def create():
    id = session.get("id")
    user = User.query.filter_by(id=id).first()

    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']

    store = Store(name=name, phone=phone, address=address, user=user)
    db.session.add(store)
    db.session.commit()

    return redirect(url_for('stores_bp.index'))


@stores_bp.route('/store/<int:id>/edit')
@check_login_in()
def edit(id):
    store = Store.query.get(id)

    return render_template('stores/edit.html', store=store)


@stores_bp.route('/store/<int:id>/update', methods=['POST'])
@check_login_in()
def update(id):
    store = Store.query.get(id)

    store.name = request.form['name']
    store.phone = request.form['phone']
    store.address = request.form['address']
    db.session.commit()

    return redirect(url_for('stores_bp.index'))


@stores_bp.route('/store/<int:id>/delete')
@check_login_in()
def delete(id):
    store = Store.query.get(id)

    db.session.delete(store)
    db.session.commit()

    return redirect(url_for('stores_bp.index'))
