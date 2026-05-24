import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class JobService {

  private http = inject(HttpClient);

  getJobs() {
    return this.http.get('/api/jobs/');
  }

  getJob(id: number) {
    return this.http.get(`/api/jobs/${id}/`);
  }

  createJob(data: any) {
    return this.http.post('/api/jobs/', data);
  }
}