System Overview
===============

NatJobs connects job seekers and recruiters with a modern full-stack web architecture.

Roles and Permissions
---------------------

- **Seeker**: Can browse open job postings, create and manage a detailed resume (experience, education, skills, languages), submit applications, track application statuses, and chat with recruiters.
- **Recruiter**: Can publish new job posts, edit or close existing listings, review applicants and their full CVs, update application statuses, and chat directly with candidates.

Real-Time WebSocket Chat
------------------------

The chat feature uses Django Channels and ASGI (Daphne). When a recruiter updates the status of an application (e.g. to Interview, Accepted, Reviewing, Rejected), the backend automatically creates or resumes a conversation with the applicant and broadcasts an instant notification.
