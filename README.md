# MediConnect — Modern Online Healthcare Platform

MediConnect is a comprehensive, full-stack healthcare platform designed to bridge the gap between patients and doctors. It provides a seamless experience for booking appointments, attending video consultations, managing medical records, and interacting with an AI-powered health assistant.

## 🚀 Key Features

- **🏥 Advanced Appointment System**: Patients can easily book appointments with specialized doctors.
- **🎥 Real-time Video Consultations**: High-quality, secure video calls using WebRTC and Socket.IO for remote diagnosis.
- **🤖 AI-Powered Chatbot (MediBot)**: Integrated with Google Gemini AI to provide instant medical guidance and symptom information.
- **💊 Digital Pharmacy**: A built-in medical store where users can browse and manage medications.
- **👤 Multi-Role Dashboard**: Tailored experiences for Patients, Doctors, and Administrators.
- **🛠 Admin Control Panel**: Manage doctor approvals, platform statistics, and system configurations.
- **🔒 Secure Authentication**: Robust user authentication and role-based access control.

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, JavaScript (Jinja2 Templates)
- **Real-time Communication**: Socket.IO, WebRTC
- **AI Integration**: Google Gemini API
- **Styling**: Vanilla CSS (Modern UI/UX)

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.11 or higher installed on your system.

### 2. Clone and Prepare Environment
```powershell
# Clone the repository (if not already done)
git clone https://github.com/reninRocky/mediconnect.git
cd mediconnect

# Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root directory (refer to `.env.example`):
```env
SECRET_KEY=your_secret_key_here
GEMINI_API_KEY=your_google_gemini_api_key
```

### 5. Run the Application
```powershell
python app.py
```
Open `http://localhost:5000` in your browser.

---

## 🔑 Default Admin Credentials
For testing and initial setup:
- **Email**: `admin@mediconnect.com`
- **Password**: `admin123`

---

## 📤 How to Push to GitHub

If you want to push your local changes to your GitHub repository, follow these steps:

1. **Initialize Git** (if you haven't already):
   ```bash
   git init
   ```

2. **Add Files**:
   Add all project files (except those ignored by `.gitignore`):
   ```bash
   git add .
   ```

3. **Commit Changes**:
   ```bash
   git commit -m "Complete project features: AI Chatbot, Video Consultation, and Medical Store"
   ```

4. **Add Remote Origin**:
   ```bash
   git remote add origin https://github.com/reninRocky/mediconnect.git
   ```

5. **Push to Main Branch**:
   ```bash
   git branch -M main
   git push -u origin main
   ```

*Note: Use `git push origin main` for subsequent updates.*

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

---
*Developed with ❤️ by [Renin Rocky](https://github.com/reninRocky)*
