import { CommonModule } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApplicationService } from '../../../../core/services/application.service';
import { AuthService } from '../../../../core/services/auth.service';
import { ChatService } from '../../../../core/services/chat.service';
import { JobService } from '../../../../core/services/job.service';

interface JobDetail {
  id: number;
  title: string;
  description: string;
  recruiter: number;
  recruiter_username?: string;
  location?: string;
  status?: string;
  has_applied?: boolean;
  application_status?: string;
}

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './job-detail.html',
  styleUrls: ['./job-detail.css'],
})
export class JobDetailComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly jobService = inject(JobService);
  private readonly applicationService = inject(ApplicationService);
  private readonly chatService = inject(ChatService);
  private readonly auth = inject(AuthService);

  readonly isRecruiter = computed(() => this.auth.role() === 'recruiter');
  readonly isSeeker = computed(() => this.auth.role() === 'seeker');
  readonly currentUser = this.auth.user;
  readonly isOwner = computed(() => {
    const user = this.currentUser();
    return this.isRecruiter() && !!user && user.id === this.job?.recruiter;
  });

  job: JobDetail | null = null;
  error = '';
  applying = false;
  startingConversation = false;
  togglingStatus = false;

  constructor() {
    const id = Number(this.route.snapshot.params['id']);

    if (!id) {
      this.error = 'Invalid job.';
      return;
    }

    this.jobService.getJob(id).subscribe({
      next: (res) => {
        this.job = res as JobDetail;
      },
      error: () => {
        this.error = 'Could not load the job.';
      },
    });
  }

  apply(): void {
    if (!this.job?.id || this.applying || !this.isSeeker() || this.job.has_applied) {
      return;
    }

    this.applying = true;
    this.error = '';

    this.applicationService.apply(this.job.id).subscribe({
      next: () => {
        this.applying = false;
        if (this.job) {
          this.job.has_applied = true;
          this.job.application_status = 'applied';
        }
        alert('Application submitted successfully.');
      },
      error: (err) => {
        this.applying = false;
        const msg = err?.error?.detail || (Array.isArray(err?.error) ? err.error[0] : 'Could not submit the application.');
        this.error = msg;
      },
    });
  }

  toggleStatus(): void {
    if (!this.job || this.togglingStatus) return;

    const newStatus = this.job.status === 'open' ? 'closed' : 'open';
    this.togglingStatus = true;

    this.jobService.updateJob(this.job.id, { status: newStatus }).subscribe({
      next: (updated: any) => {
        if (this.job) {
          this.job.status = updated.status || newStatus;
        }
        this.togglingStatus = false;
      },
      error: () => {
        this.error = 'Could not update job status.';
        this.togglingStatus = false;
      },
    });
  }

  startConversation(): void {
    const user = this.currentUser();

    if (
      !this.job ||
      !user ||
      !this.isSeeker() ||
      this.startingConversation
    ) {
      return;
    }

    this.startingConversation = true;
    this.error = '';

    this.chatService.createConversation({
      recruiter: this.job.recruiter,
      seeker: user.id,
    }).subscribe({
      next: () => {
        this.startingConversation = false;
        alert('Conversation started successfully. Open the chat widget to continue.');
      },
      error: () => {
        this.startingConversation = false;
        this.error = 'Could not start the conversation.';
      },
    });
  }
}