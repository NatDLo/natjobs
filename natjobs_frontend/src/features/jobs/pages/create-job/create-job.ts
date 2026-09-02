import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { JobService } from '../../../../core/services/job.service';

@Component({
  selector: 'app-create-job',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './create-job.html',
  styleUrls: ['./create-job.css'],
})
export class CreateJobComponent implements OnInit {
  private readonly jobService = inject(JobService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  jobId: number | null = null;
  isEditMode = false;
  loading = false;
  error = '';
  success = '';

  form = {
    title: '',
    description: '',
    location: '',
    status: 'open',
  };

  ngOnInit(): void {
    const idParam = this.route.snapshot.params['id'];
    if (idParam) {
      this.jobId = Number(idParam);
      if (this.jobId) {
        this.isEditMode = true;
        this.loadJob(this.jobId);
      }
    }
  }

  loadJob(id: number): void {
    this.loading = true;
    this.jobService.getJob(id).subscribe({
      next: (job: any) => {
        this.form = {
          title: job.title || '',
          description: job.description || '',
          location: job.location || '',
          status: job.status || 'open',
        };
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not load the job details.';
        this.loading = false;
      },
    });
  }

  publish(): void {
    if (!this.form.title.trim() || !this.form.description.trim()) {
      this.error = 'Title and description are required.';
      return;
    }

    this.loading = true;
    this.error = '';
    this.success = '';

    if (this.isEditMode && this.jobId) {
      this.jobService.updateJob(this.jobId, this.form).subscribe({
        next: () => {
          this.loading = false;
          this.success = 'Job updated successfully.';
          setTimeout(() => {
            this.router.navigateByUrl('/my-jobs');
          }, 600);
        },
        error: () => {
          this.loading = false;
          this.error = 'Could not update the job.';
        },
      });
    } else {
      this.jobService.createJob(this.form).subscribe({
        next: () => {
          this.loading = false;
          this.success = 'Job published successfully.';
          setTimeout(() => {
            this.router.navigateByUrl('/my-jobs');
          }, 600);
        },
        error: () => {
          this.loading = false;
          this.error = 'Could not publish the job.';
        },
      });
    }
  }
}