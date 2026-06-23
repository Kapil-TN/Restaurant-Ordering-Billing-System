from datetime import datetime
from ..extensions import db


class MenuItem(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", ondelete="CASCADE"),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
    db.Numeric(10, 2),
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
