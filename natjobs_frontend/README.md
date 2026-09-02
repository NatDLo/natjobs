# 🎨 NatJobs Frontend - Angular 21 Client

Modern, reactive single-page application (SPA) for the **NatJobs** recruitment platform.

---

## 🚀 Key Features

- **Angular 21 Standalone Components**: Modern component architecture without NgModules.
- **Signal-Driven & Reactive UI**: Built with Angular Signals and RxJS observables for snappy, reliable state management.
- **Real-Time WebSocket Chat**: Floating messenger widget with unread message badges, connection lifecycle handling, and auto-scroll.
- **Role-Based Routing & Guards**: `authGuard`, `guestGuard`, and `roleGuard` protecting recruiter and job-seeker views.
- **HTTP Interceptors**: Automatic Bearer JWT injection and centralized error handling.
- **Responsive Design**: Modern UI styled with CSS flexbox and grid, fully responsive across desktop and mobile.

---

## 🛠️ Tech Stack

- **Framework**: Angular 21
- **Language**: TypeScript 5.9
- **Reactive Programming**: RxJS
- **Testing**: Vitest
- **Tooling**: Angular CLI & Vite/esbuild Application Builder

---

## 🧭 Application Routes

### Public Routes
- `/auth/login` - Candidate & Recruiter sign-in
- `/auth/register` - Account creation with role selection

### Protected Routes (Authenticated)
- `/` - Open job listings with live status badges
- `/jobs/new` - Job creation form (Recruiters)
- `/jobs/:id` - Job details, recruiter contact & one-click application
- `/jobs/:id/edit` - Job edit and status toggle (`open`, `paused`, `closed`)
- `/jobs/:id/applications` - Recruiter applicant management
- `/my-jobs` - Recruiter dashboard of published jobs
- `/applications` - Candidate dashboard of submitted applications
- `/my-cv` - Seeker interactive CV builder (skills, languages, experience, education)
- `/profile` - User profile dashboard
- `/profile/edit` - User profile details editor
- `/users/:id` - Public profile & CV viewer with direct message CTA

---

## 💻 Local Development

### Prerequisites
- Node.js 20+
- npm 10+

### Setup & Run
```bash
# 1. Install dependencies
npm install

# 2. Start local development server
npm start
```

Application URL: `http://localhost:4200`

> ℹ️ **Proxy:** API (`/api`) and WebSocket (`/ws`) requests are automatically proxied to `http://127.0.0.1:8000` via `proxy.conf.json`.

### Building for Production
```bash
npm run build
```

---

## 📄 License
MIT