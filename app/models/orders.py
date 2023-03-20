from datetime import datetime
from app.extensions import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    record = db.Column(db.ARRAY(db.String), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    table = db.relationship('Table', back_populates="orders")

    def __init__(self, record, table):
        self.record = record
        self.table = table
