from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__)


def _redirect_after_login(user: User):
    if user.role == "admin":
        return redirect(url_for("admin.dashboard"))
    if user.role == "doctor":
        return redirect(url_for("doctor.dashboard"))
    return redirect(url_for("user.dashboard"))


@auth_bp.get("/login")
def login():
    if current_user.is_authenticated:
        return _redirect_after_login(current_user)  # type: ignore[arg-type]
    return render_template("auth/login.html")


@auth_bp.post("/login")
def login_post():
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        flash("Invalid email or password.", "error")
        return redirect(url_for("auth.login"))

    login_user(user)
    return _redirect_after_login(user)


@auth_bp.get("/signup")
def signup():
    if current_user.is_authenticated:
        return _redirect_after_login(current_user)  # type: ignore[arg-type]
    return render_template("auth/signup.html")


@auth_bp.post("/signup")
def signup_post():
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    if not name or not email or not password:
        flash("All fields are required.", "error")
        return redirect(url_for("auth.signup"))

    if User.query.filter_by(email=email).first():
        flash("Email already registered. Please login.", "error")
        return redirect(url_for("auth.login"))

    user = User(name=name, email=email, role="user")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return redirect(url_for("user.dashboard"))


@auth_bp.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

