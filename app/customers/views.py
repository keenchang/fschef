import os
from . import customers_bp
from app import parameters
from app.extensions import db, socketio
from app.models.stores import Store
from app.models.tables import Table, TableState
from app.models.menu_types import Menu_type
from flask_socketio import emit
from sqlalchemy import create_engine, text
from flask import render_template, request, jsonify

engine = create_engine(os.getenv('DATABASE_URL').replace("postgres:", "postgresql:"))


# 前台使用者功能
@customers_bp.route('/')
def stores():
    stores = Store.query.all()

    return render_template('customers/stores.html', stores=stores)


@customers_bp.route('/store/<int:store_id>/custom_tables')
def tables(store_id):
    tables = Table.query.filter_by(store_id=store_id).order_by(Table.id).all()

    return render_template('customers/tables.html', tables=tables, store_id=store_id)


@customers_bp.route('/store/<int:store_id>/table/<int:table_id>/menus')
def menus(store_id, table_id):
    store = Store.query.get(store_id)
    menu_types = Menu_type.query.filter_by(store_id=store_id).order_by(Menu_type.id).all()

    user_id = store.user_id
    sql_cmd = text(f"SELECT * FROM menu_type INNER JOIN menu{user_id} ON menu_type.id=menu{user_id}.menu_type_id Where store_id={store_id};")

    with engine.connect() as conn:
        menus = conn.execute(sql_cmd).fetchall()
        conn.commit()

    return render_template('customers/menus.html', menu_types=menu_types, menus=menus, 
                           user_id=user_id, store_id=store_id, table_id=table_id)


@customers_bp.route('/api/filter', methods=['POST'])
def filter():
    data = request.get_json()
    user_id = data.get('user_id')
    store_id = data.get('store_id')
    menu_type_id = data.get('menu_type_id')

    if menu_type_id == '0':
        sql_cmd = text(f"SELECT * FROM menu_type INNER JOIN menu{user_id} ON menu_type.id=menu{user_id}.menu_type_id Where store_id={store_id};")
    else:
        sql_cmd = text(f"SELECT * FROM menu_type INNER JOIN menu{user_id} ON menu_type.id=menu{user_id}.menu_type_id Where menu_type_id={menu_type_id};")

    with engine.connect() as conn:
        menus = conn.execute(sql_cmd).fetchall()
        conn.commit()

    # 讓menus變成2D list
    menus_ = []
    for row in menus:
        r = {'id': row.id, "name": row.name, "price": row.price, "img_path": row.img_path}
        menus_.append(r)

    menu_lists = []
    batch_size = 3
    for i in range(0, len(menus_), batch_size):
       menu_lists.append(menus_[i:i+batch_size])

    return jsonify({'menus': menu_lists})


@socketio.on('cart')
def handle_cart(message):
    emit(f"changeCart{message['tableId']}", message, broadcast=True)


@socketio.on('send_order')
def send_order(message):
    key_str = 'table' + message['tableId']
    table = Table.query.get(message['tableId'])

    table.status = TableState.ORDER
    db.session.commit()

    message['tableStatus'] = table.status.value
    parameters.order_list[key_str] = message

    emit('sendOrderStatus', message, broadcast=True)


@socketio.on('accept_order')
def accept_order(message):
    emit(f"acceptOrderStatus{message['tableId']}", message, broadcast=True)

