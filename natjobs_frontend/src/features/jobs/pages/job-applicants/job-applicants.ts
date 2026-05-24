import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApplicationService } from '../../../../core/services/application.service';

@Component({
  selector: 'app-job-applicants',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './job-applicants.html',
  styleUrls: ['./job-applicants.css'],
})
export class JobApplicantsComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly http = inject(HttpClient);
  private readonly applicationService = inject(ApplicationService);

  applicants: any[] = [];
  error = '';
  loading = true;
  updatingId: number | null = null;

  constructor() {
    const jobId = Number(this.route.snapshot.params['id']);

    if (!jobId) {
      this.error = 'Invalid job.';
      this.loading = false;
      return;
    }

    this.http.get<any[]>(`/api/jobs/${jobId}/applications/`).subscribe({
      next: (res) => {
        this.applicants = res;
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not load applicants.';
        this.loading = false;
      },
    });
  }

  updateStatus(applicationId: number, status: string): void {
    if (this.updatingId) {
      return;
    }

    this.updatingId = applicationId;

    this.applicationService.updateStatus(applicationId, status).subscribe({
      next: () => {
        const target = this.applicants.find((app) => app.id === applicationId);
        if (target) {
          target.status = status;
        }
        this.updatingId = null;
      },
      error: () => {
        this.error = 'Could not update application status.';
        this.updatingId = null;
      },
    });
  }
}