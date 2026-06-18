from app import create_app
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash


app = create_app()

with app.app_context():

    # Clean up existing admin to prevent IntegrityError on re-runs
    User.query.filter_by(email="admin@mail.com").delete()

    admin = User(
        name="Admin",
        email="admin@mail.com",
        password=generate_password_hash("admin123"),
        role="admin"
    )

    db.session.add(admin)

    db.session.commit()

print("Admin created")
