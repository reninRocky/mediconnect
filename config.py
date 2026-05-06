import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "mediconnect-secret-2024")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///mediconnect.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    # WebRTC ICE servers (optional TURN for "works everywhere" reliability).
    # Example:
    # TURN_URL=turn:your-domain:3478?transport=udp
    # TURN_USERNAME=mediconnect
    # TURN_PASSWORD=...
    TURN_URL = os.environ.get("TURN_URL")
    TURN_USERNAME = os.environ.get("TURN_USERNAME")
    TURN_PASSWORD = os.environ.get("TURN_PASSWORD")
