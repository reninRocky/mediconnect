from __future__ import annotations

import uuid

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from extensions import db, socketio
from models.appointment import Appointment
from models.doctor import Doctor
from models.chat import ChatHistory
from routes import role_required

user_bp = Blueprint("user", __name__)


@user_bp.get("/dashboard")
@role_required("user")
def dashboard():
    appointments = (
        Appointment.query.filter_by(user_id=current_user.id)
        .order_by(Appointment.created_at.desc())
        .limit(20)
        .all()
    )
    chats = (
        ChatHistory.query.filter_by(user_id=current_user.id)
        .order_by(ChatHistory.timestamp.desc())
        .limit(10)
        .all()
    )
    return render_template("user/dashboard.html", appointments=appointments, chats=chats)


@user_bp.get("/consult")
@role_required("user")
def consult():
    doctors = (
        Doctor.query.filter_by(is_available=True, is_approved=True)
        .order_by(Doctor.id.desc())
        .all()
    )
    return render_template("user/consult.html", doctors=doctors)


@user_bp.post("/request-call/<int:doctor_id>")
@role_required("user")
def request_call(doctor_id: int):
    doctor = Doctor.query.get_or_404(doctor_id)
    if not doctor.is_approved or not doctor.is_available:
        flash("Doctor is not available right now.", "error")
        return redirect(url_for("user.consult"))

    room_id = uuid.uuid4().hex
    appt = Appointment(user_id=current_user.id, doctor_id=doctor.id, room_id=room_id, status="pending")
    db.session.add(appt)
    db.session.commit()

    socketio.emit(
        "call_request",
        {
            "appointment_id": appt.id,
            "room_id": appt.room_id,
            "user_name": current_user.name,
        },
        room=f"doctor:{doctor.id}",
        namespace="/notifications",
    )

    flash("Call request sent. Wait for the doctor to accept.", "success")
    return redirect(url_for("user.dashboard"))

