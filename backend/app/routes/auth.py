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

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.post("/register")
def register():

    data = request.json

    user = User(
        name=data["name"],
        email=data["email"],
        password=generate_password_hash(data["password"])
    )

    db.session.add(user)

    db.session.commit()

    return {
        "message":"created"
    }


@auth_bp.post("/login")
def login():

    data = request.json

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

    user = User.query.get(int(uid))

    return {
        "id": user.id,
        "name": user.name,
        "role": user.role
    }
