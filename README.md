# 🏥 Hospital Management System

A full-stack web application that streamlines hospital operations by enabling patients to book appointments online, doctors to manage schedules and treatment notes, and admins to oversee the entire system.

> **Built for:** MAD 2 Project — IIT Madras BS in Data Science & Applications  
> **Student:** Parkhi Yadav (Roll No: 22f3002870)

---

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Background Jobs](#background-jobs)
- [Performance Optimizations](#performance-optimizations)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Demo](#demo)

---

## ❗ Problem Statement

Managing appointments manually in hospitals causes:
- Confusion and double-booking
- Long waiting delays
- Difficulty tracking patient history
- Admins struggling to organize records
- Doctors unable to easily access previous medical information

This system solves all of the above through a role-based digital platform.

---

## ✨ Features

### 👤 Patient
- Register and log in securely
- Search doctors by specialization/department
- Book or cancel appointments online
- View appointment history and treatment records
- Export treatment history as CSV

### 🩺 Doctor
- View upcoming appointments on a dashboard
- Update appointment status
- Add diagnosis and treatment notes
- View full patient medical history

### 🛠️ Admin
- View dashboard statistics (patients, doctors, appointments)
- Add and manage doctor profiles
- Search doctors and patients
- View and monitor all appointments across the system

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| Frontend | Vue.js |
| Styling | Bootstrap |
| Database | SQLite |
| ORM | SQLAlchemy |
| Caching & Message Broker | Redis |
| Background Jobs | Celery |
| HTTP Client | Axios |

---

## 🗄️ Database Schema

### Tables

| Table | Key Fields |
|---|---|
| `User` | id, name, email, password_hash, role, is_active, token, created_at |
| `Doctor` | id, user_id, department_id, is_available |
| `Patient` | id, user_id, age |
| `Department` | id, name, description |
| `Appointment` | id, doctor_id, patient_id, date, time, status |
| `Treatment` | id, appointment_id, diagnosis, prescription, notes, created_at |
| `DoctorAvailability` | id, doctor_id, date, start_time, end_time, is_booked |

### Relationships

```
User           ──(1:1)──► Doctor
User           ──(1:1)──► Patient
Department     ──(1:N)──► Doctor
Doctor         ──(1:N)──► Appointment
Patient        ──(1:N)──► Appointment
Appointment    ──(1:1)──► Treatment
Doctor         ──(1:N)──► DoctorAvailability
```

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/login` | User login |
| POST | `/api/logout` | User logout |

### Admin
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/dashboard` | Dashboard statistics |
| GET | `/api/admin/doctors` | List all doctors |
| POST | `/api/admin/doctors` | Create a doctor profile |
| GET | `/api/admin/patients` | Search patients |
| GET | `/api/admin/appointments` | View all appointments |

### Patient
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patient/register` | Patient registration |
| GET | `/api/patient/doctors` | View available doctors |
| POST | `/api/patient/appointments` | Book an appointment |
| GET | `/api/patient/history` | View treatment history |

### Doctor
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/doctor/dashboard` | Doctor dashboard |
| PUT | `/api/doctor/appointments/{id}/status` | Update appointment status |
| POST | `/api/doctor/appointments/{id}/treatment` | Add treatment details |

---

## ⚙️ Background Jobs

Powered by **Celery + Redis**:

| Job | Trigger | Description |
|---|---|---|
| Daily Reminder | Every morning | Checks today's appointments and sends reminders via Google Chat Webhooks |
| Monthly Doctor Report | 1st of every month | Generates a summary of doctor activity and appointments |
| CSV Export | On patient request | Asynchronously generates and delivers treatment history as a CSV file |

---

## 🚀 Performance Optimizations

Redis caching is implemented for frequently accessed endpoints:

- Admin dashboard statistics
- Doctor listings for patients
- Doctor dashboard appointment data

Cache expiration is configured to ensure data stays fresh and consistent.

---

## 📁 Project Structure

```
hospital-management-system/
│
├── backend/
│   ├── app.py                  # Flask app entry point
│   ├── models.py               # SQLAlchemy models
│   ├── routes/
│   │   ├── admin.py
│   │   ├── doctor.py
│   │   └── patient.py
│   ├── tasks.py                # Celery background tasks
│   └── config.py
│
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── AdminDashboard.vue
│   │   │   ├── DoctorDashboard.vue
│   │   │   └── PatientDashboard.vue
│   │   └── main.js
│   └── public/
│
└── README.md
```

---

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.8+
- Node.js & npm
- Redis server

### Backend

```bash
# Clone the repository
git clone https://github.com/your-username/hospital-management-system.git
cd hospital-management-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
flask run
```

### Celery Worker

```bash
celery -A tasks worker --loglevel=info
celery -A tasks beat --loglevel=info   # For scheduled jobs
```

### Frontend

```bash
cd frontend
npm install
npm run serve
```

### Redis

Make sure Redis is running locally:
```bash
redis-server
```

---

## 🎥 Demo

📹 [Watch the video presentation](https://drive.google.com/file/d/1P2I19ZtVWIvMwtPR8jjN9ixT9-1vriux/view?usp=sharing)

---

## 📝 Notes

- AI tools (ChatGPT) were used for ~15–20% of the work, mainly for debugging guidance, code structure improvements, and documentation formatting.
- All major implementation, integration, and debugging was completed manually.

---

## 📬 Contact

**Parkhi Yadav**  
📧 22f3002870@ds.study.iitm.ac.in  
🏫 IIT Madras — BS in Data Science & Applications 
