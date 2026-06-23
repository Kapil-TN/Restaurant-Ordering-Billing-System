from flask import (
    Blueprint,
    request
)

from app.models.user import User
from app.extensions import db

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.utils.validators import require_fields
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.post("/register")
def register():

    if not request.is_json:
        return {
            "error":"json required"
        },400

    data = request.get_json()

    if not require_fields(
        data,
        [
            "name",
            "email",
            "password"
        ]
    ):
        return {
            "error":"invalid input"
        },400

    user = User(
        name=data["name"],
        email=data["email"],
        password=generate_password_hash(data["password"])
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "error":"email exists"
        },409

    return {
        "message":"created"
    }


@auth_bp.post("/login")
def login():

    if not request.is_json:
        return {
            "error":"json required"
        },400

    data = request.get_json()

    if not require_fields(
        data,
        [
            "email",
            "password"
        ]
    ):
        return {
            "error":"invalid input"
        },400

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if not user:
        return {
            "message":"invalid"
        },401

    if not check_password_hash(
        user.password,
        data["password"]
    ):
        return {
            "message":"invalid"
        },401

    token = create_access_token(
        identity=str(user.id)
    )

    return {
        "token":token
    }


@auth_bp.get("/profile")
@jwt_required()
def profile():

    uid = get_jwt_identity()

    user = db.session.get(
        User,
        int(uid)
    )

    if not user:
        return {
            "error":"user not found"
        },401

    return {
        "id": user.id,
        "name": user.name,
        "role": user.role
    }
