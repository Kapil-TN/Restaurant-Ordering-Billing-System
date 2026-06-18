from flask import Flask
from .extensions import db, migrate
from flask_jwt_extended import JWTManager


jwt = JWTManager()


def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "sqlite:///restaurant.db"

    app.config["SECRET_KEY"] = "dev"

    app.config["JWT_SECRET_KEY"] = \
        "jwt-secret"

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .models.user import User

    from .routes.auth import auth_bp
    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    return app
