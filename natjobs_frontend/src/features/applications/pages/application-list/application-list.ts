import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApplicationService } from '../../../../core/services/application.service';

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './application-list.html',
  styleUrls: ['./application-list.css'],
})
export class ApplicationListComponent {
  private readonly applicationService = inject(ApplicationService);

  applications: any[] = [];
  error = '';
  loading = true;

  constructor() {
    this.applicationService.getMyApplications().subscribe({
      next: (res: any) => {
        this.applications = res;
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not load applications.';
        this.loading = false;
      },
    });
  }
}