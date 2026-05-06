from __future__ import annotations

from extensions import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    specialization = db.Column(db.String(120), nullable=False, default="General")
    is_available = db.Column(db.Boolean, nullable=False, default=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("User", back_populates="doctor_profile")
    appointments_as_doctor = db.relationship(
        "Appointment", back_populates="doctor", foreign_keys="Appointment.doctor_id"
    )

