import { Routes } from '@angular/router';
import { authGuard } from '../core/guards/auth.guard';
import { guestGuard } from '../core/guards/guest.guard';
import { MainLayoutComponent } from '../layout/main-layout/main-layout';

export const routes: Routes = [
  {
    path: 'auth/login',
    canActivate: [guestGuard],
    loadComponent: () =>
      import('../features/auth/pages/login/login').then((m) => m.Login),
  },
  {
    path: 'auth/register',
    canActivate: [guestGuard],
    loadComponent: () =>
      import('../features/auth/pages/register/register').then((m) => m.Register),
  },
  {
    path: '',
    component: MainLayoutComponent,
    canActivate: [authGuard],
    children: [
      {
        path: '',
        loadComponent: () =>
          import('../features/jobs/pages/job-list/job-list').then((m) => m.JobListComponent),
      },
      {
        path: 'jobs/new',
        loadComponent: () =>
          import('../features/jobs/pages/create-job/create-job').then((m) => m.CreateJobComponent),
      },
      {
        path: 'jobs/:id/edit',
        loadComponent: () =>
          import('../features/jobs/pages/create-job/create-job').then((m) => m.CreateJobComponent),
      },
      {
        path: 'jobs/:id/applications',
        loadComponent: () =>
          import('../features/jobs/pages/job-applicants/job-applicants').then(
            (m) => m.JobApplicantsComponent,
          ),
      },
      {
        path: 'jobs/:id',
        loadComponent: () =>
          import('../features/jobs/pages/job-detail/job-detail').then((m) => m.JobDetailComponent),
      },
      {
        path: 'applications',
        loadComponent: () =>
          import('../features/applications/pages/application-list/application-list').then(
            (m) => m.ApplicationListComponent,
          ),
      },
      {
        path: 'profile',
        loadComponent: () =>
          import('../features/profile/pages/profile/profile').then((m) => m.Profile),
      },
      {
        path: 'my-cv',
        loadComponent: () =>
          import('../features/profile/pages/my-cv/my-cv').then((m) => m.MyCvComponent),
      },
      {
        path: 'profile/edit',
        loadComponent: () =>
          import('../features/profile/pages/edit-profile/edit-profile').then((m) => m.EditProfile),
      },
      {
        path: 'users/:id',
        loadComponent: () =>
          import('../features/profile/pages/public-profile/public-profile').then(
            (m) => m.PublicProfileComponent,
          ),
      },
      {
        path: 'my-jobs',
        loadComponent: () =>
          import('../features/jobs/pages/my-jobs/my-jobs').then((m) => m.MyJobsComponent),
      },
    ],
  },
  {
    path: '**',
    redirectTo: '',
  },
];