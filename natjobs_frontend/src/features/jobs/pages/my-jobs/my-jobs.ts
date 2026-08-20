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

  constructor() {
    this.loadJobs();
  }

  loadJobs(): void {
    this.jobService.getJobs().subscribe({
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
}