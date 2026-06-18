import os
from flask import Flask
from .extensions import db, migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

jwt = JWTManager()


def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = \
        os.environ.get("DATABASE_URL") or "sqlite:///restaurant.db"

    app.config["SECRET_KEY"] = \
        os.environ.get("SECRET_KEY") or "dev"

    app.config["JWT_SECRET_KEY"] = \
        os.environ.get("JWT_SECRET_KEY") or "jwt-secret"

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
