import hashlib, hmac, base64, time
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


# line pay的API加密函數
def get_auth_signature (secret, uri, body, nonce):
    """
    用於製作密鑰
    :param secret: your channel secret
    :param uri: uri
    :param body: request body
    :param nonce: uuid or timestamp(時間戳)
    :return:
    """
    str_sign = secret + uri + body + nonce
    return base64.b64encode(hmac.new(str.encode(secret), str.encode(str_sign), digestmod=hashlib.sha256).digest()).decode("utf-8")


