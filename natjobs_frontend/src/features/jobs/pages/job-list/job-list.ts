import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { JobService } from '../../../../core/services/job.service';

@Component({
  selector: 'app-job-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './job-list.html',
  styleUrls: ['./job-list.css'],
})
export class JobListComponent {
  private readonly jobService = inject(JobService);

  jobs: any[] = [];
  error = '';
  loading = true;

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
        this.error = 'Could not load jobs.';
        this.loading = false;
      },
    });
  }
}