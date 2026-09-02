# 💼 NatJobs - Full Stack Recruitment & Real-Time Platform

[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.15-red?style=for-the-badge&logo=django)](https://www.django-rest-framework.org/)
[![Angular](https://img.shields.io/badge/Angular-21-DD0031?style=for-the-badge&logo=angular&logoColor=white)](https://angular.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker_Compose-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**NatJobs** is a modern full-stack recruitment web platform that seamlessly connects **Job Seekers** and **Recruiters** with end-to-end application tracking and real-time WebSocket communication.

---

## 🚀 Key Highlights & Architecture

- **Role-Based Workflows**: Distinct interfaces and capabilities tailored for **Job Seekers** and **Recruiters**.
- **Real-Time Communication**: Live bidirectional chat powered by **Django Channels**, **WebSockets**, and **Redis Channel Layers**, complete with unread notification badges and auto-messaging upon application status updates.
- **RESTful API & Security**: Robust **Django REST Framework** API secured with **JWT Authentication** (access + refresh tokens) and role guards.
- **Modern Angular Frontend**: Built with **Angular 21 standalone components**, reactive state management, signal-driven UI, interceptors, and route guards.
- **Containerized & Production Ready**: Full Docker Compose setup containing PostgreSQL, Redis, ASGI Daphne server, and Nginx.

---

## ✨ Features

### 🏢 Recruiter Experience
- **Job Management**: Create, edit, pause, and close job postings.
- **Applicant Tracking**: Review candidate profiles, full resumes, and change status (`reviewing`, `interview`, `accepted`, `rejected`).
- **Automated Chat Notifications**: Status changes instantly notify candidates via real-time chat.
- **Direct Messaging**: Chat in real-time with candidates directly from their public profiles or applicant views.

### 👤 Job Seeker Experience
- **Job Discovery**: Explore active job openings with immediate status visibility.
- **Interactive CV Builder**: Manage complete resume information (work experience, education, skills with proficiency levels, and languages).
- **One-Click Application**: Apply to open jobs with duplicate prevention and live application tracking badges (`Applied`, `Reviewing`, etc.).
- **Recruiter Contact**: Reach out to recruiters directly via profile or job detail pages.

### 💬 Real-Time Chat & Notification System
- Instant messaging via WebSockets (`/ws/chat/{id}/`).
- Live unread message counters with visual badge indicator on the floating chat widget.
- Real contact names and company info (no generic IDs).
- Message history retrieval upon joining.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Angular 21, TypeScript, RxJS, CSS3, Nginx |
| **Backend** | Python 3.8+, Django 4.2, Django REST Framework, Django Channels, Daphne, SimpleJWT |
| **Database & Cache** | PostgreSQL 15, Redis 7 (Channel Layer & Cache), SQLite (Local Dev fallback) |
| **DevOps & Tooling** | Docker, Docker Compose, Git |

---

## 🐳 Running with Docker (Recommended)

To start the full stack (PostgreSQL + Redis + Django Backend + Angular Frontend):

```bash
docker compose up --build
```

- **Frontend Application (Nginx):** [http://localhost:80](http://localhost:80)
- **Backend API & WebSockets (Daphne):** [http://localhost:8000](http://localhost:8000)
- **PostgreSQL Database:** `localhost:5432`
- **Redis Service:** `localhost:6379`

---

## 💻 Local Development Setup

### 1. Prerequisites
- Python 3.8+ (3.10+ recommended)
- Node.js 20+ & npm 10+

### 2. Backend Setup
```bash
# From repository root:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run migrations and start development server
cd backend
python manage.py migrate
python manage.py runserver
```
*Backend URL:* `http://127.0.0.1:8000`

### 3. Frontend Setup
```bash
# Open a new terminal from repository root:
cd natjobs_frontend
npm install
npm start
```
*Frontend URL:* `http://localhost:4200` *(API and WebSocket proxy configured in `proxy.conf.json`)*

---

## 🧪 Testing & Code Quality

### Backend Tests
```bash
# Run unit tests across all Django apps:
python backend/manage.py test users jobs resumes applications chat

# Coverage report:
coverage run backend/manage.py test
coverage report -m
```

### Frontend Build & Test
```bash
cd natjobs_frontend
npm test
npm run build
```

---

## 🌐 API Overview

Base URL: `/api`

| Endpoint | Method | Description |
|---|---|---|
| `/api/login/` | `POST` | Obtain JWT token pair (access + refresh) |
| `/api/refresh/` | `POST` | Refresh access token |
| `/api/users/register/` | `POST` | Register a new user (Seeker / Recruiter) |
| `/api/users/me/` | `GET`, `PATCH` | Retrieve or update authenticated profile |
| `/api/users/{id}/` | `GET` | View public user profile & CV |
| `/api/jobs/` | `GET`, `POST` | List open jobs / Create new job |
| `/api/jobs/{id}/` | `GET`, `PATCH`, `DELETE` | View, update, or close job posting |
| `/api/jobs/{id}/applications/` | `GET` | List applicants for recruiter's job |
| `/api/applications/` | `GET`, `POST` | List candidate applications / Submit application |
| `/api/applications/{id}/status/` | `PATCH` | Update application status & trigger chat notification |
| `/api/resumes/me/` | `GET`, `PATCH` | Retrieve or update seeker CV |
| `/api/chat/conversations/` | `GET` | List active chat conversations |
| `/api/chat/conversations/create/` | `POST` | Start or get 1-on-1 chat conversation |
| `/api/chat/unread-count/` | `GET` | Get total unread messages count |
| `/ws/chat/{id}/?token={JWT}` | `WebSocket` | Real-time chat connection |

---

## 📄 License

This project is licensed under the MIT License.