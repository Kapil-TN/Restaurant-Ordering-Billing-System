from flask import (
    Blueprint,
    request
)

from app.models.restaurant_table import RestaurantTable
from app.models.user import User
from app.extensions import db

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.utils.validators import require_fields
from sqlalchemy.exc import IntegrityError

table_bp = Blueprint(
    "table",
    __name__
)


@table_bp.get("")
def get_tables():

    tables = RestaurantTable.query.all()

    return [
        {
            "id": table.id,
            "table_number": table.table_number,
            "is_available": table.is_available
        }
        for table in tables
    ], 200


@table_bp.get("/<int:id>")
def get_table(id):

    table = db.session.get(RestaurantTable, id)

    if not table:
        return {
            "error": "table not found"
        }, 404

    return {
        "id": table.id,
        "table_number": table.table_number,
        "is_available": table.is_available
    }, 200


@table_bp.post("")
@jwt_required()
def create_table():

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

    if not require_fields(data, ["table_number"]):
        return {
            "error": "invalid input"
        }, 400

    table_number = data["table_number"].strip()

    if not table_number:
        return {
            "error": "invalid input"
        }, 400

    table = RestaurantTable(
        table_number=table_number
    )

    try:
        db.session.add(table)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "error": "table exists"
        }, 409

    return {
        "id": table.id,
        "table_number": table.table_number,
        "is_available": table.is_available
    }, 201


@table_bp.put("/<int:id>")
@jwt_required()
def update_table(id):

    uid = get_jwt_identity()

    current_user = db.session.get(
        User,
        int(uid)
    )

    if not current_user or current_user.role not in ["admin", "staff"]:
        return {
            "error": "unauthorized"
        }, 403

    table = db.session.get(RestaurantTable, id)

    if not table:
        return {
            "error": "table not found"
        }, 404

    if not request.is_json:
        return {
            "error": "json required"
        }, 400

    data = request.get_json()

    if not require_fields(data, ["table_number"]):
        return {
            "error": "invalid input"
        }, 400

    table_number = data["table_number"].strip()

    if not table_number:
        return {
            "error": "invalid input"
        }, 400

    table.table_number = table_number

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "error": "table exists"
        }, 409

    return {
        "id": table.id,
        "table_number": table.table_number,
        "is_available": table.is_available
    }, 200


@table_bp.delete("/<int:id>")
@jwt_required()
def delete_table(id):

    uid = get_jwt_identity()

    current_user = db.session.get(
        User,
        int(uid)
    )

    if not current_user or current_user.role not in ["admin", "staff"]:
        return {
            "error": "unauthorized"
        }, 403

    table = db.session.get(RestaurantTable, id)

    if not table:
        return {
            "error": "table not found"
        }, 404

    try:
        db.session.delete(table)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {
            "error": "failed to delete"
        }, 500

    return {
        "message": "deleted"
    }, 200


@table_bp.patch("/<int:id>/toggle")
@jwt_required()
def toggle_table(id):

    uid = get_jwt_identity()

    current_user = db.session.get(
        User,
        int(uid)
    )

    if not current_user or current_user.role not in ["admin", "staff"]:
        return {
            "error": "unauthorized"
        }, 403

    table = db.session.get(RestaurantTable, id)

    if not table:
        return {
            "error": "table not found"
        }, 404

    table.is_available = not table.is_available
    db.session.commit()

    return {
        "id": table.id,
        "table_number": table.table_number,
        "is_available": table.is_available
    }, 200
