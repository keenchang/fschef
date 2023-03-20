from . import users_bp
from app.extensions import db
from app.models.users import User
from app.sql_cmds import create_table
from flask import render_template, redirect, url_for, request, session 
from werkzeug.security import check_password_hash, generate_password_hash


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User(name=name, email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        # 註冊完成後，讓使用者是登入狀態
        session['name'] = name
        session['id'] = user.id
        session.permanent = True

        # 每個user都有一個menu table
        sql_cmd = f"""
            DROP TABLE IF EXISTS menu{user.id};
            CREATE TABLE menu{user.id} (
            id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            description TEXT,
            price INT NOT NULL,
            img_path VARCHAR(100),
            created_at TIMESTAMP NOT NULL DEFAULT NOW (),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW (),
            menu_type_id INT NOT NULL,
            FOREIGN KEY (menu_type_id) REFERENCES menu_type(id) ON DELETE CASCADE
            )
        """
        create_table("public", f"""menu{user.id}""", sql_cmd)

        return redirect(url_for('stores_bp.index'))

    return render_template('users/register.html')


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()

        if user and check_password_hash(user.password, password):
            session['name'] = name
            session['id'] = user.id
            session.permanent = True

            return redirect(url_for('stores_bp.index'))
        else:
            return render_template('users/login.html')
    
    return render_template('users/login.html')


@users_bp.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('id', None)

    return redirect(url_for('stores_bp.index'))
