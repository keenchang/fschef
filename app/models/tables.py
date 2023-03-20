from datetime import datetime
from app.extensions import db
import enum

class TableState(enum.Enum):
    NOT_ORDER = "未點餐"
    ORDER = "已點餐"
    ACCEPT = "已接受"
    CANCEL = "已取消"
    PAY = "已付款"

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.Enum(TableState), nullable=False, default=TableState.NOT_ORDER)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    store = db.relationship('Store', back_populates="tables")
    orders = db.relationship('Order', back_populates='table', cascade="all, delete")

    def __init__(self, name, store):
        self.name = name
        self.store = store
