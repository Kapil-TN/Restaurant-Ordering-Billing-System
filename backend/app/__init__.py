from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate, jwt
from .config import Config


def create_app():

    app = Flask(__name__)

    # Load configuration from Config object
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Enable CORS for the frontend port
    CORS(
        app,
        origins=[
            "http://localhost:5173"
        ]
    )

    from .models.user import User

    from .routes.auth import auth_bp
    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    return app
