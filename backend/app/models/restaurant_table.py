from datetime import datetime
from ..extensions import db


class RestaurantTable(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    table_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    is_available = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
