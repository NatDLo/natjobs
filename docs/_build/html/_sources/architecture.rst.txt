Architecture & Technologies
===========================

Backend Architecture
--------------------

- **Django 4.2 & Django REST Framework**: Exposes RESTful endpoints with serializers and role-based permissions.
- **Django Channels & Daphne**: Provides asynchronous WebSocket connection handling for real-time chat with JWT query authentication.
- **PostgreSQL & Redis**: Persistent data storage in PostgreSQL and distributed message brokering via Redis channel layers.

Frontend Architecture
---------------------

- **Angular 21**: Standalone component architecture with reactive state signals and RxJS streams.
- **Nginx**: Production reverse proxy handling HTTP API proxying, WebSocket upgrading, and Angular SPA fallback routing.
