# ⚙️ NatJobs Backend API & WebSocket Service

Django REST Framework & Django Channels backend powering the **NatJobs** recruitment platform.

---

## 🛠️ Tech Stack & Architecture

- **Framework**: Django 4.2 & Django REST Framework (DRF)
- **Authentication**: SimpleJWT (JWT tokens: access + refresh)
- **Real-Time Communication**: Django Channels 4 & Daphne ASGI Server
- **Message Broker / Cache**: Redis 7 / Channel Layers
- **Database**: PostgreSQL 15 (Docker) / SQLite (Local fallback)
- **Testing**: Django Test Suite & Coverage

---

## 📁 App Structure

```text
backend/
├── applications/    # Application submission, tracking & automated notification signals
├── chat/            # WebSocket consumers, conversation routing, unread counts & JWT middleware
├── jobs/            # Job postings CRUD, status toggling, permissions & role querysets
├── resumes/         # Seeker CV management (skills, experience, education, languages)
├── users/           # Custom User model (Seeker vs Recruiter), signals & profile handlers
├── backend/         # Root settings, ASGI router, WSGI & URL configuration
└── manage.py
```

---

## 📡 API Reference

Base URL: `/api`

### 🔑 Authentication
- `POST /api/login/` - Authenticate and retrieve JWT token pair
- `POST /api/refresh/` - Refresh JWT access token

### 👥 Users
- `POST /api/users/register/` - Register account (`seeker` or `recruiter`)
- `GET /api/users/me/` - Retrieve own profile
- `PATCH /api/users/me/` - Update profile & recruiter company details
- `GET /api/users/{id}/` - Retrieve public user profile and public CV

### 💼 Jobs
- `GET /api/jobs/` - List open jobs (or recruiter's own jobs)
- `POST /api/jobs/` - Publish a new job (Recruiters only)
- `GET /api/jobs/{id}/` - Retrieve job posting details
- `PATCH /api/jobs/{id}/` - Update job details or change status (`open`, `paused`, `closed`)
- `DELETE /api/jobs/{id}/` - Remove job posting (Owner recruiter only)
- `GET /api/jobs/{id}/applications/` - List candidate applications for this job

### 📄 Resumes & Candidate CVs (Seeker Only)
- `POST /api/resumes/` - Create candidate resume
- `GET /api/resumes/me/` - Get candidate's own resume
- `PATCH /api/resumes/me/` - Update resume summary and availability
- Nested resources for skills, languages, experiences, and education under `/api/resumes/...`

### 📝 Applications
- `GET /api/applications/` - List candidate's submitted applications
- `POST /api/applications/` - Submit application for an open job (Includes resume snapshot)
- `GET /api/applications/{id}/` - View application details
- `PATCH /api/applications/{id}/status/` - Update status (`reviewing`, `interview`, `accepted`, `rejected`) + triggers automated chat notification

### 💬 Real-Time Chat & Messages
- `GET /api/chat/conversations/` - List all active conversations with unread counter and contact details
- `POST /api/chat/conversations/create/` - Create or retrieve 1-on-1 chat room (`user_id` or `recruiter`/`seeker`)
- `GET /api/chat/conversations/{id}/` - View conversation details
- `POST /api/chat/conversations/{id}/read/` - Mark conversation messages as read
- `GET /api/chat/unread-count/` - Total unread message badge count

---

## 🔌 WebSocket Specification

**Endpoint:** `ws://<host>/ws/chat/<conversation_id>/?token=<JWT_ACCESS_TOKEN>`

- **Authentication**: JWT token validated in ASGI middleware (`JwtAuthMiddleware`).
- **Authorization**: Connection accepted only if authenticated user is a participant.
- **On Connect**: Delivers recent message history and marks pending messages as read.
- **On Message**: Broadcasts new messages via channel layer to the conversation group.

---

## 💻 Running Backend Locally

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Run migrations
python manage.py migrate

# 3. Start development server
python manage.py runserver
```

### Running Tests
```bash
python manage.py test users jobs resumes applications chat
```

---

## 📄 License
MIT