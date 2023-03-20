import numpy as np
import os, requests, json, uuid
from flask import render_template, request, jsonify, url_for, redirect
from . import orders_bp
from app import parameters
from app.extensions import db, socketio
from app.models.orders import Order
from app.models.stores import Store
from app.models.tables import Table, TableState
from app.utils import check_login_in, get_auth_signature

# line pay api的headers參數
channel_id = os.environ.get('CHANNEL_ID')
channel_secret = os.environ.get('CHANNEL_SECRET')
uri = "/v3/payments/request"
nonce = str(uuid.uuid4())

# 藍新金流api的參數
# mpg_merchant_id = os.environ.get('MPG_MERCHANT_ID')
# mpg_iv = os.environ.get('MPG_IV')
# mpg_key = os.environ.get('MPG_KEY')


@orders_bp.route('/table/<int:table_id>/order/new')
@check_login_in()
def new(table_id):
    table = Table.query.get(table_id)

    key_str = 'table' + str(table_id)
    if key_str in parameters.order_list:
        order_infos = parameters.order_list[key_str]

        order_infos.pop('storeId', None)
        order_infos.pop('tableId', None)
        order_infos.pop('tableStatus', None)
        order_infos.pop('msg', None)
    
        return render_template('orders/new.html', order_infos=order_infos, table=table)
    else:
        table.status = TableState.NOT_ORDER
        db.session.commit()

        return redirect(url_for('tables_bp.index', store_id=table.store_id))


@orders_bp.route('/api/order/create', methods=['POST'])
@check_login_in()
def create():
    data = request.get_json()

    table_id = data.get('tableId')
    table = Table.query.get(table_id)

    key_str = 'table' + str(table_id)
    order_infos = parameters.order_list[key_str]

    order_infos.pop('storeId', None)
    order_infos.pop('tableId', None)
    order_infos.pop('tableStatus', None)

    record = []
    for k, v in order_infos.items():
        record.append([str(k), str(v['count'])])
    
    try:
        table.status = TableState.ACCEPT
        db.session.commit()

        order = Order(record=record, table=table)
        db.session.add(order)
        db.session.commit()

        return jsonify({'tableStatus': table.status.value, 
                        'url': url_for('tables_bp.index', store_id=table.store_id), 
                        'orderId': order.id})
    except Exception as e:
        db.session.rollback()

        return jsonify({'message': str(e)}), 500


@orders_bp.route('/api/order/cancel', methods=['POST'])
@check_login_in()
def cancel():
    data = request.get_json()
    table_id = data.get('tableId')

    table = Table.query.get(table_id)
    table.status = TableState.CANCEL
    db.session.commit()
    
    try:
        return jsonify({'tableStatus': table.status.value, 
                        'url': url_for('tables_bp.index', store_id=table.store_id)})
    except Exception as e:
        db.session.rollback()

        return jsonify({'message': str(e)}), 500


@orders_bp.route('/order/<int:order_id>/pay')
def pay(order_id):
    order = Order.query.get(order_id)
    table = Table.query.get(order.table_id)
    store = Store.query.get(table.store_id)

    records = order.record
    id_list, num_list = '', []
    for record in records:
        num_list.append(int(record[1]))
        id_list += record[0] + ','
    id_list = id_list[:-1] 

    sql_cmd = f"SELECT name, price FROM menu{store.user_id} WHERE id IN (" + id_list + ")"
    menu_infos = db.engine.execute(sql_cmd).fetchall()
    menu_infos = np.array(menu_infos).T.tolist()

    name_list = menu_infos[0]
    price_list = menu_infos[1]
    price_list = [int(x) for x in price_list]

    amount = np.sum(np.array(price_list) * np.array(num_list))
    products_name = "餐點"

    product_list = []
    for idx, num in enumerate(num_list):
        item = {"name": name_list[idx]}
        item["quantity"] = num
        item["price"] = price_list[idx]

        product_list.append(item)

    url = os.environ.get('URL') + "/order/{order_id}/checkout".format(order_id = order.id)
    form_data = {
        "amount": str(amount),
        "currency": 'TWD',
        "orderId": str(order.id),
        "packages": [
            {
                "id": str(order.id),
                "amount": str(amount),
                "name": products_name,
                "products": product_list
            }
        ],
        "redirectUrls": {
            "confirmUrl": url,
            "cancelUrl": url
        }
    }
    json_body = json.dumps(form_data)

    headers = {
        'Content-Type': 'application/json',
        'X-LINE-ChannelId': channel_id,
        'X-LINE-Authorization-Nonce': nonce,
        'X-LINE-Authorization': get_auth_signature(channel_secret, uri, json_body, nonce) 
    }

    response = requests.post("https://sandbox-api-pay.line.me" + uri, headers=headers, data=json_body)
    dict_response = json.loads(response.text)

    if dict_response.get('returnCode') == "0000":
        info = dict_response.get('info')
        web_url = info.get('paymentUrl').get('web')

        return redirect(web_url)
    else:
        return redirect(url_for('menus', store_id=table.store_id, table_id=table.id))


# @orders_bp.route('/order/<int:order_id>/blue_pay')
# def blue_pay(order_id):
#     order = Order.query.get(order_id)

#     records = order.record
#     id_list, num_list = '', []
#     for record in records:
#         num_list.append(int(record[1]))
#         id_list += record[0] + ','
#     id_list = id_list[:-1]        

#     sql_cmd = f"SELECT name, price FROM menu5 WHERE id IN (" + id_list + ")"
#     menu_infos = db.engine.execute(sql_cmd).fetchall()
#     menu_infos = np.array(menu_infos).T.tolist()

#     name_list = menu_infos[0]
#     price_list = menu_infos[1]
#     price_list = [int(x) for x in price_list]

#     amount = np.sum(np.array(price_list) * np.array(num_list))
#     products_name = "餐點"

#     data = {
#         "order_id": order.id, 
#         "amount": amount, 
#         "products_name": products_name, 
#         "email": "test@gmail.com", 
#         "ReturnURL": "https://tw.news.yahoo.com/", 
#         "NotifyURL": "https://tw.news.yahoo.com/"
#     }
#     form_info = mpg(mpg_key, mpg_iv, mpg_merchant_id, data).gen_form_info()

#     return render_template("orders/newebpay.html", form_info=form_info)


@orders_bp.route('/order/<int:order_id>/checkout')
def checkout(order_id):
    order = Order.query.get(order_id)
    table = Table.query.get(order.table_id)

    table.status = TableState.PAY
    db.session.commit()

    message = { "storeId": table.store_id, "tableId": table.id, "tableStatus": table.status.value }
    socketio.emit("sendOrderStatus", message, broadcast=True)

    return redirect(url_for('customers_bp.menus', store_id=table.store_id, table_id=table.id))

