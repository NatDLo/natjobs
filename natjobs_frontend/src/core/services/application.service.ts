import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ApplicationService {
  private readonly http = inject(HttpClient);

  apply(jobId: number) {
    return this.http.post('/api/applications/', {
      job_id: jobId,
    });
  }

  getMyApplications() {
    return this.http.get('/api/applications/');
  }

  updateStatus(applicationId: number, status: string, notes = '') {
    return this.http.patch(`/api/applications/${applicationId}/status/`, {
      status,
      notes,
    });
  }
}