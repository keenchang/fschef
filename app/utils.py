import hashlib, hmac, base64, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
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


# 藍新金流的API
class mpg():
    def __init__(self, mpg_key, mpg_iv, mpg_id, data):
        self.mpg_key = mpg_key
        self.mpg_iv = mpg_iv
        self.mpg_id = mpg_id
        self.info = {}

        self.set_info(data)
    
    def gen_form_info(self):
        form_info = {
            "merchant_id": self.mpg_id,
            "trade_info": self.gen_trade_info(self.info),
            "trade_sha": self.gen_trade_sha(self.trade_info),
            "version": "2.0"
        }
        
        return form_info
    
    def gen_trade_info(self, data):
        parse_data = self.gen_query_string(data)
        self.trade_info = self.mpg_aes_encrypt(parse_data.encode())

        return self.trade_info
    
    def gen_trade_sha(self, data):
        trade_sha = self.mpg_sha_encrypt(data)

        return trade_sha

    def set_info(self, data):
        self.info["MerchantID"] = self.mpg_id
        self.info["MerchantOrderNo"] = data["order_id"]
        self.info["Amt"] = data["amount"]
        self.info["ItemDesc"] = data["products_name"]
        self.info["Email"] = data["email"]
        self.info["TimeStamp"] = str(int(time.time()))
        self.info["RespondType"] = "JSON"
        self.info["Version"] = "2.0"
        self.info["LoginType"] = 0
        self.info["CREDIT"] = 1
        self.info["VACC"] = 1
        self.info["ReturnURL"] = data["ReturnURL"]
        self.info["NotifyURL"] = data["NotifyURL"]
    
    def gen_query_string(self, data):
        new_string = ""

        for k, v in data.items():
            new_string += k + "=" + str(v) + "&"

        new_string = new_string[:-1]

        return new_string

    def mpg_aes_encrypt(self, data):
        cipher = AES.new(self.mpg_key.encode(), AES.MODE_CBC, iv=self.mpg_iv.encode())
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    
        return ct_bytes.hex()
    
    def mpg_sha_encrypt(self, data):
        plain_text = "HashKey=" + self.mpg_key + "&" + data + "&HashIV=" + self.mpg_iv
        m = hashlib.sha256()
        m.update(plain_text.encode())

        return m.hexdigest().upper()

