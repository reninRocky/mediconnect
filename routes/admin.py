from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db
from models.appointment import Appointment
from models.doctor import Doctor
from models.medical_store import Medicine
from models.user import User
from routes import role_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/dashboard")
@role_required("admin")
def dashboard():
    users = User.query.order_by(User.id.desc()).limit(50).all()
    doctors = Doctor.query.order_by(Doctor.id.desc()).limit(50).all()
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(50).all()
    medicines = Medicine.query.order_by(Medicine.id.desc()).limit(50).all()

    stats = {
        "users": User.query.count(),
        "doctors": Doctor.query.count(),
        "appointments": Appointment.query.count(),
        "medicines": Medicine.query.count(),
    }
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        users=users,
        doctors=doctors,
        appointments=appointments,
        medicines=medicines,
    )


@admin_bp.get("/register-doctor")
@role_required("admin")
def register_doctor():
    return render_template("admin/register_doctor.html")


@admin_bp.post("/register-doctor")
@role_required("admin")
def register_doctor_post():
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    specialization = (request.form.get("specialization") or "General").strip()

    if not name or not email or not password:
        flash("All fields are required.", "error")
        return redirect(url_for("admin.register_doctor"))

    if User.query.filter_by(email=email).first():
        flash("Email already exists.", "error")
        return redirect(url_for("admin.register_doctor"))

    user = User(name=name, email=email, role="doctor")
    user.set_password(password)
    db.session.add(user)
    db.session.flush()  # get user.id

    doctor = Doctor(user_id=user.id, specialization=specialization, is_available=False, is_approved=False)
    db.session.add(doctor)
    db.session.commit()

    flash("Doctor registered. Approve them from the dashboard.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.post("/approve-doctor/<int:doctor_id>")
@role_required("admin")
def approve_doctor(doctor_id: int):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.is_approved = True
    db.session.commit()
    flash("Doctor approved.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.post("/medicine/add")
@role_required("admin")
def add_medicine():
    name = (request.form.get("name") or "").strip()
    description = (request.form.get("description") or "").strip()
    price = float(request.form.get("price") or 0)
    stock = int(request.form.get("stock") or 0)
    image_url = (request.form.get("image_url") or "").strip() or None

    if not name:
        flash("Medicine name is required.", "error")
        return redirect(url_for("admin.dashboard"))

    med = Medicine(name=name, description=description, price=price, stock=stock, image_url=image_url)
    db.session.add(med)
    db.session.commit()
    flash("Medicine added.", "success")
    return redirect(url_for("admin.dashboard"))

