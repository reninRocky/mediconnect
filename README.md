# MediConnect — Online Hospital Platform

## Quick start (Windows)

1) Install Python 3.11+ and reopen PowerShell.

If `python` says “Python was not found…”, either:

- Use the Python launcher: run `py --version` and use `py` instead of `python`, or
- Disable the Microsoft Store alias: **Settings → Apps → Advanced app settings → App execution aliases** → turn off `python.exe` and `python3.exe`.

2) Create & activate a virtual environment:

```powershell
cd "d:\medical project\mediconnect"
py -m venv venv
venv\Scripts\activate
```

3) Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4) Create `.env` (copy from `.env.example`) and set:

- `SECRET_KEY`
- `GEMINI_API_KEY` (optional; chatbot works with a helpful message if missing)

5) Run:

```powershell
python app.py
```

### One-command setup scripts (recommended)

```powershell
cd "d:\medical project\mediconnect"
.\setup-windows.ps1
.\run.ps1
```

Then open:

- Home: `http://localhost:5000`
- Login: `http://localhost:5000/login`

## Default admin

- Email: `admin@mediconnect.com`
- Password: `admin123`

## Notes

- Doctors are created + approved by the admin panel.
- Video calls use WebRTC with Socket.IO signaling (no TURN server configured).
- On Windows/Python 3.13, Socket.IO runs in `threading` async mode for compatibility (instead of `eventlet`).
- SQLite DB file `mediconnect.db` is created on first run.

"# mediconnect" 
