from flask import (
    Blueprint,
    request
)

from app.models.category import Category
from app.models.user import User
from app.extensions import db

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.utils.validators import require_fields
from sqlalchemy.exc import IntegrityError

category_bp = Blueprint(
    "category",
    __name__
)


@category_bp.get("")
def get_categories():

    categories = Category.query.all()

    return [
        {
            "id": c.id,
            "name": c.name
        }
        for c in categories
    ], 200


@category_bp.get("/<int:id>")
def get_category(id):

    category = db.session.get(Category, id)

    if not category:
        return {
            "error": "category not found"
        }, 404

    return {
        "id": category.id,
        "name": category.name
    }, 200


@category_bp.post("")
@jwt_required()
def create_category():

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

    if not require_fields(data, ["name"]):
        return {
            "error": "invalid input"
        }, 400

    name = data["name"].strip()

    if not name:
        return {
            "error": "invalid input"
        }, 400

    category = Category(
        name=name
    )

    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "error": "category exists"
        }, 409

    return {
        "id": category.id,
        "name": category.name
    }, 201


@category_bp.put("/<int:id>")
@jwt_required()
def update_category(id):

    uid = get_jwt_identity()

    current_user = db.session.get(
        User,
        int(uid)
    )

    if not current_user or current_user.role not in ["admin", "staff"]:
        return {
            "error": "unauthorized"
        }, 403

    category = db.session.get(Category, id)

    if not category:
        return {
            "error": "category not found"
        }, 404

    if not request.is_json:
        return {
            "error": "json required"
        }, 400

    data = request.get_json()

    if not require_fields(data, ["name"]):
        return {
            "error": "invalid input"
        }, 400

    name = data["name"].strip()

    if not name:
        return {
            "error": "invalid input"
        }, 400

    category.name = name

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "error": "category exists"
        }, 409

    return {
        "id": category.id,
        "name": category.name
    }, 200


@category_bp.delete("/<int:id>")
@jwt_required()
def delete_category(id):

    uid = get_jwt_identity()

    current_user = db.session.get(
        User,
        int(uid)
    )

    if not current_user or current_user.role not in ["admin", "staff"]:
        return {
            "error": "unauthorized"
        }, 403

    category = db.session.get(Category, id)

    if not category:
        return {
            "error": "category not found"
        }, 404

    try:
        db.session.delete(category)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {
            "error": "failed to delete"
        }, 500

    return {
        "message": "deleted"
    }, 200
