from datetime import datetime
from app.extensions import db

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates="stores")
    menu_types = db.relationship('Menu_type', back_populates='store', cascade="all, delete")
    tables = db.relationship('Table', back_populates='store', cascade="all, delete")


    def __init__(self, name, phone, address, user):
        self.name = name
        self.phone = phone
        self.address = address
        self.user = user

