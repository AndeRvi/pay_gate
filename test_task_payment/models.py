from datetime import datetime
from . import db


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_order_id = db.Column(db.String(36), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

