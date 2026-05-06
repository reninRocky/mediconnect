from __future__ import annotations

from flask import Blueprint, render_template

from models.medical_store import Medicine
from routes import role_required

store_bp = Blueprint("store", __name__)


@store_bp.get("/")
@role_required("user", "doctor", "admin")
def store():
    medicines = Medicine.query.order_by(Medicine.id.desc()).all()
    return render_template("store/store.html", medicines=medicines)


@store_bp.get("/cart")
@role_required("user", "doctor", "admin")
def cart():
    return render_template("store/cart.html")

