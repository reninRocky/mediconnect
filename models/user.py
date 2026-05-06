from __future__ import annotations

from flask_login import UserMixin

from extensions import bcrypt, db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # user|doctor|admin

    doctor_profile = db.relationship("Doctor", back_populates="user", uselist=False)
    appointments_as_user = db.relationship(
        "Appointment", back_populates="user", foreign_keys="Appointment.user_id"
    )
    chats = db.relationship("ChatHistory", back_populates="user")

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

