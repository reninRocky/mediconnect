from __future__ import annotations

import uuid

from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import bcrypt, db, login_manager, socketio


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    socketio.init_app(app, cors_allowed_origins="*")
    bcrypt.init_app(app)

    # Import models so SQLAlchemy registers all tables before create_all().
    from models.user import User  # noqa: F401
    from models.doctor import Doctor  # noqa: F401
    from models.appointment import Appointment  # noqa: F401
    from models.medical_store import Medicine  # noqa: F401
    from models.chat import ChatHistory  # noqa: F401

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.doctor import doctor_bp
    from routes.admin import admin_bp
    from routes.chatbot import chatbot_bp
    from routes.store import store_bp
    from routes.video import video_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(doctor_bp, url_prefix="/doctor")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(chatbot_bp, url_prefix="/chat")
    app.register_blueprint(store_bp, url_prefix="/store")
    app.register_blueprint(video_bp, url_prefix="/video")

    @app.get("/")
    def index():
        from flask import render_template

        return render_template("index.html")

    def create_admin():
        from models.user import User

        admin = User.query.filter_by(email="admin@mediconnect.com").first()
        if admin:
            return
        admin = User(
            name="Admin",
            email="admin@mediconnect.com",
            role="admin",
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

    with app.app_context():
        db.create_all()
        create_admin()

    @app.context_processor
    def inject_globals():
        return {"uuid4": lambda: str(uuid.uuid4())}

    return app


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True)
