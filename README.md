# NatJobs

NatJobs is a full-stack recruitment platform that connects recruiters and job seekers.

Recruiters can publish jobs and manage incoming applications.
Seekers can build a complete CV, apply to jobs, and chat in real time with recruiters.

## Project Overview

This repository contains two applications:

- Backend: Django + Django REST Framework + Channels (WebSocket)
- Frontend: Angular 21

Main folders:

- backend application in [backend](backend)
- frontend application in [natjobs_frontend](natjobs_frontend)
- Python dependencies in [requirements.txt](requirements.txt)

## Core Features

### Authentication and Authorization

- JWT login and refresh flow
- Role-based access: recruiter and seeker
- Protected routes and role-aware API behavior

### Recruiter Features

- View own published jobs
- Create new job postings
- Review applications per job
- Update application status (reviewing, interview, accepted, rejected)
- Chat with seekers

### Seeker Features

- Browse open jobs
- Build and edit full CV (resume, skills, languages, experience, education)
- Apply to open jobs
- Track own applications
- Chat with recruiters

### Real-Time Communication

- WebSocket chat through Django Channels
- JWT token-based socket authentication
- Conversation history and live message broadcast

## Tech Stack

### Backend

- Django 4.2
- Django REST Framework
- SimpleJWT
- Django Channels + Daphne
- SQLite (default)
- Optional Redis channel layer/cache

### Frontend

- Angular 21
- TypeScript
- RxJS
- Vitest
- Angular CLI

## Backend API (High Level)

Base path: /api

- Auth: /api/login, /api/refresh
- Users: /api/users
- Resumes: /api/resumes
- Jobs: /api/jobs
- Applications: /api/applications
- Chat: /api/chat

WebSocket endpoint:

- /ws/chat/{conversation_id}/?token={JWT_ACCESS_TOKEN}

## Local Development Setup

### 1. Prerequisites

- Python 3.10+ recommended
- Node.js 20+
- npm 10+

### 2. Backend Setup

From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Run backend:

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

Backend URL:

- http://127.0.0.1:8000

### 3. Frontend Setup

Open a second terminal from repository root:

```bash
cd natjobs_frontend
npm install
npm start
```

Frontend URL:

- http://localhost:4200

The frontend proxies API and WebSocket traffic using [natjobs_frontend/proxy.conf.json](natjobs_frontend/proxy.conf.json).

## Testing

### Backend tests

From [backend](backend):

```bash
python manage.py test
```

Run coverage:

```bash
coverage erase
coverage run manage.py test
coverage report -m
coverage html
```

### Frontend tests

From [natjobs_frontend](natjobs_frontend):

```bash
npm test
```

## Environment Notes

Backend settings are in [backend/backend/settings.py](backend/backend/settings.py).

Useful variables:

- DJANGO_SECRET_KEY
- DJANGO_DEBUG
- DJANGO_ALLOWED_HOSTS
- USE_REDIS
- REDIS_CHANNEL_URL
- REDIS_CACHE_URL

Defaults are development-friendly (SQLite + in-memory channels/cache).

## Frontend Scripts

Scripts are defined in [natjobs_frontend/package.json](natjobs_frontend/package.json):

- npm start
- npm run build
- npm run watch
- npm test

## Recommended Validation Flow

1. Register one recruiter and one seeker user.
2. Recruiter publishes a job.
3. Seeker creates CV and applies.
4. Recruiter reviews applications.
5. Both users open conversation and exchange messages.

## Notes

- Keep secrets out of Git (.env, local DB, node_modules, build artifacts).
- Python 3.8 may show cryptography deprecation warnings; prefer Python 3.10+ for long-term compatibility.

## License

MIT