# 📄 PaperTrail — University Document Tracking System

> A centralized document-tracking web application designed to give university students and personnel real-time visibility over academic requests, clearances, and office approvals.

---

## 📌 Problem Statement

Students frequently submit documents that require signatures and endorsements across multiple campus offices. Because tracking is traditionally manual, applicants often do not know where their paperwork is or whether an action is pending. This leads to repeated physical follow-ups, lost time, and delayed submissions. 

**PaperTrail** resolves this by providing transparency, clear stage history, and dynamic workflow tracking.

---

## 🏗️ Architecture: Vertical Slicing

This project is built using the **Vertical Slicing (Package-by-Feature)** architecture rather than traditional horizontal layer grouping. Each business capability owns its views, URLs, models, templates, and static assets.

```text
PaperTrail/
│
├── apps/
│   ├── login/            # 🔐 Authentication & Session Management
│   ├── register/         # 📝 Student Account Creation
│   ├── home/             # 🏠 Central Dashboard Experience
│   ├── profile/          # 👤 User Profile Management
│   ├── user_settings/    # ⚙️ User Preferences & Notifications
│   └── __init__.py       # Package initialization
│
├── papertrail/           # ⚙️ Core Configuration (settings, root urls)
│
├── static/
│   ├── css/              # Feature-specific CSS stylesheets
│   ├── images/           # Feature-specific media & icons
│   └── js/               # Feature-specific client-side scripts
│
├── templates/
│   ├── login/            # Login screen templates
│   ├── register/         # Registration screen templates
│   ├── home/             # Dashboard screen templates
│   ├── profile/          # Profile screen templates
│   └── user_settings/    # Settings screen templates
│
├── .env                  # Environment Variables (Protected credentials)
├── .gitignore            # Git exclusion rules
├── manage.py             # Django CLI runner
└── requirements.txt      # Project dependencies
```
## ✨ Features Implemented
* 🔐 Login Feature (apps/login): Secure authentication and session verification.
* 📝 Register Feature (apps/register): Automated creation of student user accounts, base profile, and default preferences.
* 🏠 Home Dashboard (apps/home): Landing screen displaying active user status, feature quick-access cards, and secure logout.
* 👤 Profile Feature (apps/profile): Read and update user profile information (full_name, bio) linked via a OneToOneField to Django's User model.
* ⚙️ User Settings (apps/user_settings): Manage account preferences (dark_mode, email_notifications).
* ☁️ Cloud Database: Hosted PostgreSQL backend connected via Supabase.

## 🛠️ Tech Stack
* Backend Framework: Django (Python 3.x)
* Database: PostgreSQL (Hosted on Supabase)
* Database Driver / Adapter: psycopg[binary], dj-database-url
* Configuration Management: python-dotenv
* Frontend: Django Template Language (DTL), HTML5, Pure CSS3, JavaScript

## 🚀 Getting Started
Follow these steps to run the project locally on your machine:
## 1. Clone the Repository
```bash
git clone https://github.com/trealcoseba/PaperTrailApp.git
cd PaperTrailApp
```
## 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```
## 3. Install Dependencies
```bash
pip install -r requirements.txt
```
## 4. Configure Environment Variables
Create a .env file in the project root:
```bash
DATABASE_URL=postgresql://postgres.<PROJECT_REF>:<PASSWORD>@<POOLER_HOST>:5432/postgres
```
## 5. Run Migrations & Start Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
## Open your browser and visit:
👉 http://127.0.0.1:8000/

## 👤 Author

**Lemuel Vincent Alcoseba III**
* 🎓 **Program:** BS Computer Science
* 🐙 **GitHub:** [@trealcoseba](https://github.com/trealcoseba)
* 💼 **Project:** CSIT327 Final Project
