from flask import session, redirect, url_for


# 確認使用者是否登入
def check_login_in():
    def decorator(func):
        def wrap(*args, **kw):
            name = session.get("name")

            if name == None or name == '':
                return redirect(url_for('users_bp.register'))
            else:
                return func(*args, **kw)
        
        wrap.__name__ = func.__name__
        return wrap
 
    return decorator