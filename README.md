# Volunteer Management System (Flask + MongoDB)

## 📌 Overview
The **Volunteer Management System** is a web application built using **Flask**, **MongoDB**, **HTML**, and **CSS** — without JavaScript.  
It allows organizations to manage volunteers, roles, shifts, availability, file uploads, notifications, and reporting in a simple, responsive interface.

---

## 🚀 Features
1. **User Authentication & Roles** – Email/password login with MongoDB storage, role-based access (Admin / Volunteer).
2. **Real-Time Notifications** – Email/SMS shift reminders with logging in MongoDB.
3. **Dynamic Role & Shift Creation** – Admins can add/edit roles and shifts via the web interface.
4. **Volunteer Availability Calendar** – Volunteers mark availability; matched with shifts.
5. **Event Dashboards** – See assignments, coverage, and attendance statistics.
6. **File Uploads** – Store volunteer documents securely in MongoDB GridFS.
7. **Search & Filter** – Locate volunteers by name, role, or availability.
8. **Volunteer Portal** – View assigned roles, shifts, and attendance history.
9. **Automated Reminders** – Schedule notifications with Celery.
10. **Analytics & Reporting** – Generate insights using MongoDB aggregations.
11. **Responsive Design** – Works on desktops, tablets, and mobiles.
12. **Conflict Detection** – Avoid overlapping shifts with MongoDB validation.

---

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Database:** MongoDB
- **Frontend:** HTML + CSS
- **File Storage:** MongoDB GridFS
- **Optional Notifications:** Flask-SocketIO / Twilio
- **Task Scheduling:** Celery (optional)

---

## 📂 Project Structure
Volunteer-Management-System/
│── app.py # Main Flask application
│── requirements.txt # Python dependencies
│── templates/ # HTML templates
│── static/ # CSS styles
│── uploads/ # Temporary uploaded files
│── README.md # Documentation

---

## ⚙️ Setup Instructions

### 1️⃣ Install Requirements

pip install -r requirements.txt


2️⃣ MongoDB Connection
In app.py, configure your MongoDB:


app.config["MONGO_URI"] = "mongodb://localhost:27017/volunteer_db"


3️⃣ Run the Application
python app.py
Open http://127.0.0.1:5000 in your browser.
