from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))


class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    table_id = db.Column(db.Integer, nullable=True)
    order_type = db.Column(db.String(20))
    status = db.Column(db.String(20))
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)
    served_at = db.Column(db.DateTime, nullable=True)


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Float)
    subtotal = db.Column(db.Float)


class Bill(db.Model):
    __tablename__ = 'bill'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    total_amount = db.Column(db.Float)
    tax_amount = db.Column(db.Float)
    discount = db.Column(db.Float)
    grand_total = db.Column(db.Float)
    payment_mode = db.Column(db.String(20))
    billed_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))
