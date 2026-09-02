import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { JobService } from '../../../../core/services/job.service';

@Component({
  selector: 'app-my-jobs',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './my-jobs.html',
  styleUrls: ['./my-jobs.css'],
})
export class MyJobsComponent {
  private readonly jobService = inject(JobService);

  jobs: any[] = [];
  loading = true;
  error = '';
  updatingId: number | null = null;

  constructor() {
    this.loadJobs();
  }

  loadJobs(): void {
    this.loading = true;
    this.jobService.getMyJobs().subscribe({
      next: (res: any) => {
        this.jobs = Array.isArray(res) ? res : [];
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not load your jobs.';
        this.loading = false;
      },
    });
  }

  toggleJobStatus(job: any): void {
    if (this.updatingId === job.id) return;
    const newStatus = job.status === 'open' ? 'closed' : 'open';
    this.updatingId = job.id;

    this.jobService.updateJob(job.id, { status: newStatus }).subscribe({
      next: (updated: any) => {
        job.status = updated.status || newStatus;
        this.updatingId = null;
      },
      error: () => {
        this.error = `Could not ${newStatus === 'closed' ? 'close' : 'reopen'} the job.`;
        this.updatingId = null;
      },
    });
  }
}