# NatJobs Frontend

Angular frontend for NatJobs, a recruitment platform connecting recruiters and seekers through job posts, applications, resumes, and real-time chat.

## Features

- JWT-based login and registration flow
- Route guards for authenticated and guest users
- Role-aware views (recruiter vs seeker)
- Job list and job detail pages
- Job applicants page for recruiters
- Applications page for seekers
- Profile, edit profile, and public profile pages
- Real-time chat using WebSocket
- Local API and WS proxy for development

## Tech Stack

- Angular 21
- TypeScript
- RxJS
- Vitest
- Angular CLI

## Routes

### Public routes
- /auth/login
- /auth/register

### Protected routes
- /
- /jobs/:id
- /jobs/:id/applications
- /applications
- /profile
- /profile/edit
- /users/:id

## API and WebSocket Integration

- API base path: /api
- WebSocket base path: /ws

Proxy config (development):
- /api -> http://127.0.0.1:8000
- /ws -> http://127.0.0.1:8000 (ws enabled)

This lets frontend and backend run on different ports without CORS issues during development.

## Local Development

Requirements:
- Node.js 20+
- npm 10+

Install:

    npm install

Run dev server:

    npm start

Frontend URL:
- http://localhost:4200

Build:

    npm run build

Tests:

    npm test

## Scripts

- npm start
- npm run build
- npm run watch
- npm test

## Recommended Workflow

1. Start backend on port 8000
2. Start frontend on port 4200
3. Login as recruiter or seeker
4. Validate main flows:
   - Recruiter creates jobs
   - Seeker creates resume and applies to jobs
   - Both users open a conversation and chat in real time

## License

MIT