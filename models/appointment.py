from __future__ import annotations

from datetime import datetime

from extensions import db


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False, index=True)

    status = db.Column(db.String(20), nullable=False, default="pending")  # pending|active|done|declined
    room_id = db.Column(db.String(64), nullable=False, unique=True, index=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="appointments_as_user", foreign_keys=[user_id])
    doctor = db.relationship(
        "Doctor", back_populates="appointments_as_doctor", foreign_keys=[doctor_id]
    )

