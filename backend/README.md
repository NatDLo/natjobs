# NatJobs Backend

Django REST API and WebSocket backend for NatJobs, a recruitment platform where recruiters publish jobs and seekers apply using their resumes.

## Features

- JWT authentication (login + refresh)
- Custom user roles: recruiter and seeker
- Recruiter job management
- Seeker resume management:
  - Resume profile
  - Skills
  - Languages
  - Experience
  - Education
- Job applications workflow with status updates
- Real-time chat between recruiter and seeker using Django Channels + WebSocket
- SQLite by default, optional Redis for channels and cache

## Tech Stack

- Django 4.2
- Django REST Framework
- SimpleJWT
- Django Channels + Daphne
- SQLite (default)
- Redis (optional, for production-like async and caching)

## Project Structure

backend/
- backend/ (settings, URLs, ASGI/WSGI)
- users/
- jobs/
- resumes/
- applications/
- chat/
- manage.py

Main API routing:
- backend/backend/urls.py

WebSocket setup:
- backend/backend/asgi.py
- backend/chat/routing.py
- backend/chat/consumers.py

## API Overview

Base path: /api

### Authentication
- POST /api/login/
- POST /api/refresh/

### Users
- POST /api/users/register/
- GET/PATCH /api/users/me/
- GET /api/users/{id}/

### Jobs
- GET/POST /api/jobs/
- GET /api/jobs/{id}/
- PATCH/DELETE /api/jobs/{id}/update/
- GET /api/jobs/{id}/applications/

### Resumes
- GET/POST /api/resumes/
- GET/PATCH /api/resumes/me/
- GET/PATCH/DELETE /api/resumes/{id}/
- Nested resources for skills, languages, experiences, and education under resumes

### Applications
- GET/POST /api/applications/
- GET /api/applications/{id}/
- PATCH /api/applications/{id}/status/

### Chat
- GET /api/chat/conversations/
- POST /api/chat/conversations/create/
- GET /api/chat/conversations/{id}/

## WebSocket Chat

Endpoint:
- /ws/chat/{conversation_id}/?token={JWT_ACCESS_TOKEN}

Rules:
- User must be authenticated with JWT token in query string
- User must belong to the conversation
- On connect, server sends the latest message history
- New messages are broadcast to all participants in the conversation room

## Environment Variables

Supported variables:
- DJANGO_SECRET_KEY
- DJANGO_DEBUG (true or false)
- DJANGO_ALLOWED_HOSTS (comma-separated)
- USE_REDIS (1 to enable Redis, 0 otherwise)
- REDIS_CHANNEL_URL (default: redis://127.0.0.1:6379/0)
- REDIS_CACHE_URL (default: redis://127.0.0.1:6379/1)

Defaults are development-friendly (SQLite + in-memory channel layer + local cache).

## Local Development

Requirements:
- Python 3.10+
- pip

Install:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r ../requirements.txt

Run:

    python manage.py migrate
    python manage.py runserver

Backend URL:
- http://127.0.0.1:8000

## Notes

- Authentication is required for most endpoints
- Role-based permissions are enforced in views

## License

MIT