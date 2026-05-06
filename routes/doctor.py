from __future__ import annotations

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from extensions import db, socketio
from models.appointment import Appointment
from models.doctor import Doctor
from routes import role_required

doctor_bp = Blueprint("doctor", __name__)


def _current_doctor() -> Doctor:
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    if not doctor:
        abort(403)
    return doctor


@doctor_bp.get("/dashboard")
@role_required("doctor")
def dashboard():
    doctor = _current_doctor()
    pending = (
        Appointment.query.filter_by(doctor_id=doctor.id, status="pending")
        .order_by(Appointment.created_at.desc())
        .all()
    )
    today = (
        Appointment.query.filter_by(doctor_id=doctor.id)
        .order_by(Appointment.created_at.desc())
        .limit(20)
        .all()
    )
    return render_template("doctor/dashboard.html", doctor=doctor, pending=pending, today=today)


@doctor_bp.post("/toggle-availability")
@role_required("doctor")
def toggle_availability():
    doctor = _current_doctor()
    if not doctor.is_approved:
        flash("Your account is pending approval.", "error")
        return redirect(url_for("doctor.dashboard"))

    doctor.is_available = not doctor.is_available
    db.session.commit()
    flash("Availability updated.", "success")
    return redirect(url_for("doctor.dashboard"))


@doctor_bp.post("/accept/<int:appointment_id>")
@role_required("doctor")
def accept(appointment_id: int):
    doctor = _current_doctor()
    appt = Appointment.query.get_or_404(appointment_id)
    if appt.doctor_id != doctor.id:
        abort(403)

    appt.status = "active"
    db.session.commit()

    socketio.emit(
        "call_accepted",
        {"room_id": appt.room_id, "appointment_id": appt.id},
        room=f"user:{appt.user_id}",
        namespace="/notifications",
    )

    return redirect(url_for("video.room", room_id=appt.room_id))


@doctor_bp.post("/decline/<int:appointment_id>")
@role_required("doctor")
def decline(appointment_id: int):
    doctor = _current_doctor()
    appt = Appointment.query.get_or_404(appointment_id)
    if appt.doctor_id != doctor.id:
        abort(403)

    appt.status = "declined"
    db.session.commit()
    socketio.emit(
        "call_declined",
        {"appointment_id": appt.id},
        room=f"user:{appt.user_id}",
        namespace="/notifications",
    )
    flash("Declined request.", "success")
    return redirect(url_for("doctor.dashboard"))

