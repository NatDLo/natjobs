import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { API_BASE_URL } from '../config/api-config';
import {
  Resume,
  UpdateResumeDto,
  CreateSkillDto,
  CreateLanguageDto,
  CreateExperienceDto,
  CreateEducationDto,
  Skill,
  Language,
  Experience,
  Education,
} from '../../features/auth/auth-module';

@Injectable({ providedIn: 'root' })
export class ResumeService {
  private readonly http = inject(HttpClient);

  getMyResume() {
    return this.http.get<Resume>(`${API_BASE_URL}/resumes/me/`);
  }

  createResume(data: UpdateResumeDto) {
    return this.http.post<Resume>(`${API_BASE_URL}/resumes/`, data);
  }

  updateMyResume(data: UpdateResumeDto) {
    return this.http.patch<Resume>(`${API_BASE_URL}/resumes/me/`, data);
  }

  addSkill(resumeId: number, data: CreateSkillDto) {
    return this.http.post<Skill>(`${API_BASE_URL}/resumes/${resumeId}/skills/`, data);
  }

  updateSkill(skillId: number, data: Partial<CreateSkillDto>) {
    return this.http.patch<Skill>(`${API_BASE_URL}/resumes/skills/${skillId}/`, data);
  }

  deleteSkill(skillId: number) {
    return this.http.delete(`${API_BASE_URL}/resumes/skills/${skillId}/`);
  }

  addLanguage(resumeId: number, data: CreateLanguageDto) {
    return this.http.post<Language>(`${API_BASE_URL}/resumes/${resumeId}/languages/`, data);
  }

  updateLanguage(languageId: number, data: Partial<CreateLanguageDto>) {
    return this.http.patch<Language>(`${API_BASE_URL}/resumes/languages/${languageId}/`, data);
  }

  deleteLanguage(languageId: number) {
    return this.http.delete(`${API_BASE_URL}/resumes/languages/${languageId}/`);
  }

  addExperience(resumeId: number, data: CreateExperienceDto) {
    return this.http.post<Experience>(`${API_BASE_URL}/resumes/${resumeId}/experiences/`, data);
  }

  updateExperience(experienceId: number, data: Partial<CreateExperienceDto>) {
    return this.http.patch<Experience>(`${API_BASE_URL}/resumes/experiences/${experienceId}/`, data);
  }

  deleteExperience(experienceId: number) {
    return this.http.delete(`${API_BASE_URL}/resumes/experiences/${experienceId}/`);
  }

  addEducation(resumeId: number, data: CreateEducationDto) {
    return this.http.post<Education>(`${API_BASE_URL}/resumes/${resumeId}/education/`, data);
  }

  updateEducation(educationId: number, data: Partial<CreateEducationDto>) {
    return this.http.patch<Education>(`${API_BASE_URL}/resumes/education/${educationId}/`, data);
  }

  deleteEducation(educationId: number) {
    return this.http.delete(`${API_BASE_URL}/resumes/education/${educationId}/`);
  }
}