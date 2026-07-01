from flask import (
    Blueprint,
    request
)

from app.models.menu_item import MenuItem
from app.models.category import Category
from app.models.user import User
from app.extensions import db

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.utils.validators import require_fields

menu_bp = Blueprint(
    "menu",
    __name__
)


@menu_bp.get("")
def get_menu_items():

    items = MenuItem.query.all()

    return [
        {
            "id": item.id,
            "name": item.name,
            "price": float(item.price),
            "is_available": item.is_available,
            "category_id": item.category_id,
            "category_name": item.category.name
        }
        for item in items
    ], 200


@menu_bp.get("/<int:id>")
def get_menu_item(id):

    item = db.session.get(MenuItem, id)

    if not item:
        return {
            "error": "item not found"
        }, 404

    return {
        "id": item.id,
        "name": item.name,
        "price": float(item.price),
        "is_available": item.is_available,
        "category_id": item.category_id,
        "category_name": item.category.name
    }, 200


@menu_bp.post("")
@jwt_required()
def create_menu_item():

    uid = get_jwt_identity()

    current_user = db.session.get(
        User,
        int(uid)
    )

    if not current_user or current_user.role not in ["admin", "staff"]:
        return {
            "error": "unauthorized"
        }, 403

    if not request.is_json:
        return {
            "error": "json required"
        }, 400

    data = request.get_json()

    if not require_fields(
        data,
        [
            "name",
            "price",
            "category_id"
        ]
    ):
        return {
            "error": "invalid input"
        }, 400

    name = data["name"].strip()

    if not name:
        return {
            "error": "invalid input"
        }, 400

    try:
        price = float(data["price"])
    except (ValueError, TypeError):
        return {
            "error": "invalid input"
        }, 400

    if price <= 0:
        return {
            "error": "invalid input"
        }, 400

    category_id = data["category_id"]

    category = db.session.get(
        Category,
        category_id
    )

    if not category:
        return {
            "error": "category not found"
        }, 404

    item = MenuItem(
        name=name,
        price=price,
        category_id=category_id
    )

    db.session.add(item)
    db.session.commit()

    return {
        "id": item.id,
        "name": item.name,
        "price": float(item.price),
        "is_available": item.is_available,
        "category_id": item.category_id,
        "category_name": item.category.name
    }, 201


@menu_bp.put("/<int:id>")
@jwt_required()
def update_menu_item(id):

    uid = get_jwt_identity()

    current_user = db.session.get(
        User,
        int(uid)
    )

    if not current_user or current_user.role not in ["admin", "staff"]:
        return {
            "error": "unauthorized"
        }, 403

    item = db.session.get(MenuItem, id)

    if not item:
        return {
            "error": "item not found"
        }, 404

    if not request.is_json:
        return {
            "error": "json required"
        }, 400

    data = request.get_json()

    if "name" in data:
        name = data["name"].strip()
        if not name:
            return {
                "error": "invalid input"
            }, 400
        item.name = name

    if "price" in data:
        try:
            price = float(data["price"])
        except (ValueError, TypeError):
            return {
                "error": "invalid input"
            }, 400
        if price <= 0:
            return {
                "error": "invalid input"
            }, 400
        item.price = price

    if "category_id" in data:
        category = db.session.get(
            Category,
            data["category_id"]
        )
        if not category:
            return {
                "error": "category not found"
            }, 404
        item.category_id = data["category_id"]

    if "is_available" in data:
        if not isinstance(
            data["is_available"],
            bool
        ):
            return {
                "error": "invalid input"
            }, 400
        item.is_available = data["is_available"]

    db.session.commit()

    return {
        "id": item.id,
        "name": item.name,
        "price": float(item.price),
        "is_available": item.is_available,
        "category_id": item.category_id,
        "category_name": item.category.name
    }, 200


@menu_bp.delete("/<int:id>")
@jwt_required()
def delete_menu_item(id):

    uid = get_jwt_identity()

    current_user = db.session.get(
        User,
        int(uid)
    )

    if not current_user or current_user.role not in ["admin", "staff"]:
        return {
            "error": "unauthorized"
        }, 403

    item = db.session.get(MenuItem, id)

    if not item:
        return {
            "error": "item not found"
        }, 404

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {
            "error": "failed to delete"
        }, 500

    return {
        "message": "deleted"
    }, 200


@menu_bp.patch("/<int:id>/toggle")
@jwt_required()
def toggle_menu_item(id):

    uid = get_jwt_identity()

    current_user = db.session.get(
        User,
        int(uid)
    )

    if not current_user or current_user.role not in ["admin", "staff"]:
        return {
            "error": "unauthorized"
        }, 403

    item = db.session.get(MenuItem, id)

    if not item:
        return {
            "error": "item not found"
        }, 404

    item.is_available = not item.is_available
    db.session.commit()

    return {
        "id": item.id,
        "name": item.name,
        "is_available": item.is_available
    }, 200
