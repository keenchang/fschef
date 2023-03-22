import os, shutil
from . import menus_bp
from app.extensions import db
from app.models.menu_types import Menu_type
from app.utils import check_login_in
from flask import render_template, redirect, url_for, request, current_app, session
from sqlalchemy import create_engine, text

engine = create_engine(os.getenv('DATABASE_URL').replace("postgres", "postgresql"))


@menus_bp.route('/menu_type/<int:menu_type_id>/menus')
@check_login_in()
def index(menu_type_id):
    menu_type = Menu_type.query.get(menu_type_id)

    user_id = session.get("id")
    sql_cmd = text(f"SELECT * FROM menu{user_id} WHERE menu_type_id = {menu_type_id} ORDER BY id")
    with engine.connect() as conn:
        menus = conn.execute(sql_cmd).fetchall()
        conn.commit()

    return render_template("menus/index.html", menus=menus, store_id=menu_type.store_id)


@menus_bp.route('/menu_type/<int:menu_type_id>/menu/new')
@check_login_in()
def new(menu_type_id):
    return render_template("menus/new.html", menu_type_id=menu_type_id)


@menus_bp.route('/menu_type/<int:menu_type_id>/menu/create', methods=['POST'])
@check_login_in()
def create(menu_type_id):
    user_id = session.get("id")
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    img = request.files['img']

    sql_cmd = text(f"INSERT INTO menu{user_id} (name, description, price, menu_type_id) VALUES ('{name}', '{description}', '{price}', '{menu_type_id}') RETURNING id".replace("%", "%%"))

    with engine.connect() as conn:
        [menu_id] = conn.execute(sql_cmd).fetchone()
        conn.commit()

    if img.filename != '':
        # 把圖片路徑寫入Menu
        sql_cmd = text(f"UPDATE menu{user_id} SET img_path = '{os.path.join(current_app.config['UPLOAD_FOLDER'], str(menu_id), img.filename)}' WHERE id = {menu_id}")

        with engine.connect() as conn:
            conn.execute(sql_cmd)
            conn.commit()

        # 把圖片存到static/img/{menu_id}內
        save_dir = os.path.join(current_app.static_folder, 
                                current_app.config['UPLOAD_FOLDER'], 
                                str(menu_id))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        img.save(os.path.join(save_dir, img.filename))

    return redirect(url_for('menus_bp.index', menu_type_id=menu_type_id))


@menus_bp.route('/menu/<int:id>/edit')
@check_login_in()
def edit(id):
    user_id = session.get("id")

    sql_cmd = text(f"SELECT * FROM menu{user_id} WHERE id = {id}")
    with engine.connect() as conn:
        menu = conn.execute(sql_cmd).fetchone()
        conn.commit()

    return render_template('menus/edit.html', menu=menu)


@menus_bp.route('/menu/<int:id>/update', methods=['POST'])
@check_login_in()
def update(id):
    user_id = session.get("id")
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    img = request.files['img']

    sql_cmd = text(f"UPDATE menu{user_id} SET name = '{name}', description = '{description}', price = '{price}' WHERE id = {id} RETURNING id, menu_type_id".replace("%", "%%"))

    with engine.connect() as conn:
        [menu_id, menu_type_id] = conn.execute(sql_cmd).fetchone()
        conn.commit()

    if img.filename != '':
        # 把圖片路徑寫入Menu
        sql_cmd = text(f"UPDATE menu{user_id} SET img_path = '{os.path.join(current_app.config['UPLOAD_FOLDER'], str(menu_id), img.filename)}' WHERE id = {menu_id}")

        with engine.connect() as conn:
            conn.execute(sql_cmd)
            conn.commit()

        # 把圖片存到static/img/{menu_id}內
        save_dir = os.path.join(current_app.static_folder, 
                                current_app.config['UPLOAD_FOLDER'], 
                                str(menu_id))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        img.save(os.path.join(save_dir,  img.filename))

    return redirect(url_for('menus_bp.index', menu_type_id=menu_type_id))


@menus_bp.route('/menus/<int:id>/delete')
@check_login_in()
def delete(id):
    user_id = session.get("id")

    sql_cmd = text(f"SELECT * FROM menu{user_id} WHERE id = {id}")
    with engine.connect() as conn:
        menu = conn.execute(sql_cmd).fetchone()
        conn.commit()
    menu_type_id = menu.menu_type_id

    if menu.img_path != None:
        shutil.rmtree(os.path.join(current_app.static_folder, 
                                   current_app.config['UPLOAD_FOLDER'], 
                                   str(menu.id)))

    sql_cmd = text(f"DELETE FROM menu{user_id} WHERE id = {id}")

    with engine.connect() as conn:
        conn.execute(sql_cmd)
        conn.commit()

    return redirect(url_for('menus_bp.index', menu_type_id=menu_type_id))

