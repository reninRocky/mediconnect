from __future__ import annotations

from flask import Blueprint, current_app, jsonify, render_template, request
from flask_login import current_user

from extensions import db
from models.chat import ChatHistory
from routes import role_required

chatbot_bp = Blueprint("chatbot", __name__)

SYSTEM_PROMPT = """You are MediBot, a helpful medical assistant for MediConnect Hospital.
Provide general medical information, symptom guidance, and health tips.
Always recommend consulting a real doctor for serious conditions.
Avoid giving definitive diagnoses; be cautious and safety-focused."""


@chatbot_bp.get("/")
@role_required("user", "doctor", "admin")
def chat_page():
    return render_template("chatbot/chat.html")


@chatbot_bp.post("/ask")
@role_required("user", "doctor", "admin")
def ask():
    user_msg = (request.json or {}).get("message", "")
    user_msg = (user_msg or "").strip()
    if not user_msg:
        return jsonify({"reply": "Please type a message."}), 400

    api_key = current_app.config.get("GEMINI_API_KEY")
    if not api_key:
        reply = "Gemini API key is missing. Set `GEMINI_API_KEY` in your `.env` and restart the server."
        return jsonify({"reply": reply}), 200

    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    try:
        resp = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser: {user_msg}")
        reply = (getattr(resp, "text", None) or "").strip() or "Sorry, I couldn't generate a reply."
    except Exception as e:  # noqa: BLE001
        reply = f"Chatbot error: {e}"

    if current_user.is_authenticated:
        db.session.add(ChatHistory(user_id=current_user.id, message=user_msg, response=reply))
        db.session.commit()

    return jsonify({"reply": reply})

