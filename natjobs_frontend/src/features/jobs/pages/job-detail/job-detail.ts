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

  job: JobDetail | null = null;
  error = '';
  applying = false;
  startingConversation = false;

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
    if (!this.job?.id || this.applying || !this.isSeeker()) {
      return;
    }

    this.applying = true;
    this.error = '';

    this.applicationService.apply(this.job.id).subscribe({
      next: () => {
        this.applying = false;
        alert('Application submitted successfully.');
      },
      error: () => {
        this.applying = false;
        this.error = 'Could not submit the application.';
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