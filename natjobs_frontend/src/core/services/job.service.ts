import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class JobService {
  private http = inject(HttpClient);

  getJobs(params?: { mine?: boolean | string }) {
    return this.http.get<any[]>('/api/jobs/', { params: params as any });
  }

  getMyJobs() {
    return this.http.get<any[]>('/api/jobs/', { params: { mine: 'true' } });
  }

  getJob(id: number) {
    return this.http.get<any>(`/api/jobs/${id}/`);
  }

  createJob(data: any) {
    return this.http.post<any>('/api/jobs/', data);
  }

  updateJob(id: number, data: any) {
    return this.http.patch<any>(`/api/jobs/${id}/`, data);
  }

  deleteJob(id: number) {
    return this.http.delete<any>(`/api/jobs/${id}/`);
  }
}