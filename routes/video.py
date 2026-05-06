from __future__ import annotations

import json

from flask import Blueprint, abort, current_app, render_template
from flask_login import current_user
from flask_socketio import join_room, leave_room

from extensions import socketio
from models.appointment import Appointment
from models.doctor import Doctor
from routes import role_required

video_bp = Blueprint("video", __name__)


@video_bp.get("/room/<string:room_id>")
@role_required("user", "doctor", "admin")
def room(room_id: str):
    appt = Appointment.query.filter_by(room_id=room_id).first()
    if not appt:
        abort(404)

    allowed = False
    if current_user.role == "admin":
        allowed = True
    elif current_user.role == "user" and appt.user_id == current_user.id:
        allowed = True
    elif current_user.role == "doctor":
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if doctor and appt.doctor_id == doctor.id:
            allowed = True

    if not allowed:
        abort(403)

    # Perfect-negotiation pattern needs a deterministic "polite" side.
    # Make doctors/admin polite; users impolite. This avoids offer-collision issues.
    is_polite = current_user.role in {"doctor", "admin"}

    ice_servers = [{"urls": "stun:stun.l.google.com:19302"}]
    turn_url = current_app.config.get("TURN_URL")
    if turn_url:
        ice_servers.append(
            {
                "urls": turn_url,
                "username": current_app.config.get("TURN_USERNAME"),
                "credential": current_app.config.get("TURN_PASSWORD"),
            }
        )

    return render_template(
        "user/video_call.html",
        room_id=room_id,
        is_polite=is_polite,
        ice_servers_json=json.dumps(ice_servers),
    )


# ---------------------------
# Notifications namespace
# ---------------------------


@socketio.on("join_user", namespace="/notifications")
def on_join_user(data):
    user_id = (data or {}).get("user_id")
    if user_id is not None:
        join_room(f"user:{user_id}")


@socketio.on("join_doctor", namespace="/notifications")
def on_join_doctor(data):
    doctor_id = (data or {}).get("doctor_id")
    if doctor_id is not None:
        join_room(f"doctor:{doctor_id}")


# ---------------------------
# WebRTC signaling namespace
# ---------------------------


@socketio.on("join_room", namespace="/video")
def on_join_room(data):
    room = (data or {}).get("room")
    if room:
        join_room(room)


@socketio.on("leave_room", namespace="/video")
def on_leave_room(data):
    room = (data or {}).get("room")
    if room:
        leave_room(room)


@socketio.on("offer", namespace="/video")
def on_offer(data):
    room = (data or {}).get("room")
    if room:
        socketio.emit("offer", data, room=room, include_self=False, namespace="/video")


@socketio.on("answer", namespace="/video")
def on_answer(data):
    room = (data or {}).get("room")
    if room:
        socketio.emit("answer", data, room=room, include_self=False, namespace="/video")


@socketio.on("ice-candidate", namespace="/video")
def on_ice(data):
    room = (data or {}).get("room")
    if room:
        socketio.emit("ice-candidate", data, room=room, include_self=False, namespace="/video")


@socketio.on("end_call", namespace="/video")
def on_end_call(data):
    room = (data or {}).get("room")
    if room:
        socketio.emit("end_call", {}, room=room, namespace="/video")

