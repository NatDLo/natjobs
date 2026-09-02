Welcome to NatJobs's Documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   architecture
   modules

Overview
--------

NatJobs is a recruitment platform that allows recruiters to post job openings and manage candidate applications, while job seekers can build a comprehensive CV, apply to open roles, and communicate with recruiters in real time using WebSockets.

Key Features:
- Role-based Authentication & JWT Authorization (Recruiter / Seeker).
- Full CV builder with skills, languages, experience, and education.
- Real-time chat via Django Channels and WebSocket consumers.
- Automated chat notifications upon application status updates.
- Docker & Docker Compose setup with PostgreSQL and Redis.
