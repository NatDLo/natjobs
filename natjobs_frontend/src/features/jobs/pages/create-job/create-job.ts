import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { JobService } from '../../../../core/services/job.service';

@Component({
  selector: 'app-create-job',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './create-job.html',
  styleUrls: ['./create-job.css'],
})
export class CreateJobComponent {
  private readonly jobService = inject(JobService);
  private readonly router = inject(Router);

  loading = false;
  error = '';
  success = '';

  form = {
    title: '',
    description: '',
    location: '',
    status: 'open',
  };

  publish(): void {
    if (!this.form.title.trim() || !this.form.description.trim()) {
      this.error = 'Title and description are required.';
      return;
    }

    this.loading = true;
    this.error = '';
    this.success = '';

    this.jobService.createJob(this.form).subscribe({
      next: () => {
        this.loading = false;
        this.success = 'Job published successfully.';
        this.router.navigateByUrl('/my-jobs');
      },
      error: () => {
        this.loading = false;
        this.error = 'Could not publish the job.';
      },
    });
  }
}