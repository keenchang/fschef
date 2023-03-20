from . import tables_bp
from app import parameters
from app.extensions import db
from app.models.stores import Store
from app.models.tables import Table, TableState
from app.utils import check_login_in
from flask import render_template, redirect, url_for, request


@tables_bp.route('/store/<int:store_id>/tables')
@check_login_in()
def index(store_id):
    tables = Table.query.filter_by(store_id=store_id).order_by(Table.id).all()

    return render_template("tables/index.html", tables=tables, store_id=store_id)


@tables_bp.route('/store/<int:store_id>/table/new')
@check_login_in()
def new(store_id):
    return render_template("tables/new.html", store_id=store_id)


@tables_bp.route('/store/<int:store_id>/table/create', methods=['POST'])
@check_login_in()
def create(store_id):
    store = Store.query.get(store_id)

    name = request.form['name']

    table = Table(name=name, store=store)
    db.session.add(table)
    db.session.commit()

    return redirect(url_for('tables_bp.index', store_id=store_id))


@tables_bp.route('/table/<int:id>/edit')
@check_login_in()
def edit(id):
    table = Table.query.get(id)

    return render_template('tables/edit.html', table=table)


@tables_bp.route('/table/<int:id>/update', methods=['POST'])
@check_login_in()
def update(id):
    table = Table.query.get(id)

    table.name = request.form['name']
    db.session.commit()

    return redirect(url_for('tables_bp.index', store_id=table.store_id))


@tables_bp.route('/table/<int:id>/delete')
@check_login_in()
def delete(id):
    table = Table.query.get(id)
    store_id = table.store_id

    db.session.delete(table)
    db.session.commit()

    return redirect(url_for('tables_bp.index', store_id=store_id))


@tables_bp.route('/table/<int:id>/clear')
@check_login_in()
def clear(id):
    table = Table.query.get(id)

    table.status = TableState.NOT_ORDER
    db.session.commit()

    key_str = 'table' + str(id)
    if key_str in parameters.order_list:
        parameters.order_list[key_str] = {}

    return redirect(url_for('tables_bp.index', store_id=table.store_id))

