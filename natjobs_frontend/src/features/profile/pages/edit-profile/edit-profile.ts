import { Component, computed, effect, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { forkJoin } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import {
  CreateEducationDto,
  CreateExperienceDto,
  CreateLanguageDto,
  CreateSkillDto,
  Resume,
  UpdateResumeDto,
} from '../../../auth/auth-module';
import { AuthService } from '../../../../core/services/auth.service';
import { ResumeService } from '../../../../core/services/resume.service';

@Component({
  selector: 'app-edit-profile',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './edit-profile.html',
  styleUrls: ['./edit-profile.css'],
})
export class EditProfile {
  private readonly auth = inject(AuthService);
  private readonly resumeService = inject(ResumeService);
  private readonly router = inject(Router);

  readonly user = this.auth.user;
  readonly isSeeker = computed(() => this.auth.role() === 'seeker');
  readonly isRecruiter = computed(() => this.auth.role() === 'recruiter');

  loading = false;
  error = '';
  success = '';
  resumeId: number | null = null;

  userForm = {
    email: '',
    first_name: '',
    last_name: '',
    company_name: '',
  };

  resumeForm: UpdateResumeDto = {
    full_name: '',
    location: '',
    phone: '',
    photo: null,
    bio: '',
    availability: '',
    mobility: false,
  };

  skillForm: CreateSkillDto = {
    name: '',
    level: 1,
  };

  languageForm: CreateLanguageDto = {
    name: '',
    level: 'beginner',
  };

  experienceForm: CreateExperienceDto = {
    job_title: '',
    company: '',
    start_date: '',
    end_date: '',
    description: '',
  };

  educationForm: CreateEducationDto = {
    institution: '',
    degree: '',
    start_date: '',
    end_date: '',
  };

  constructor() {
    effect(() => {
      const user = this.user();

      if (!user) {
        return;
      }

      this.userForm = {
        email: user.email ?? '',
        first_name: user.first_name ?? '',
        last_name: user.last_name ?? '',
        company_name: user.recruiter_profile?.company_name ?? '',
      };

      const resume = user.seeker_profile?.resume ?? null;
      this.resumeId = resume?.id ?? null;

      if (resume) {
        this.patchResumeForm(resume);
      }
    });
  }

  save(): void {
    const user = this.user();

    if (!user || this.loading) {
      return;
    }

    this.error = '';
    this.success = '';

    if (this.isSeeker()) {
      if (
        !this.resumeForm.full_name?.trim() ||
        !this.resumeForm.location?.trim() ||
        !this.resumeForm.phone?.trim()
      ) {
        this.error = 'Full name, location, and phone are required.';
        return;
      }
    }

    this.loading = true;

    if (this.isRecruiter()) {
      this.auth.updateMe(this.userForm).subscribe({
        next: () => {
          this.loading = false;
          this.success = 'Profile updated successfully.';
          this.router.navigate(['/profile']);
        },
        error: () => {
          this.loading = false;
          this.error = 'Could not update the profile.';
        },
      });

      return;
    }

    if (!this.isSeeker()) {
      this.loading = false;
      this.error = 'User role is not ready yet. Please try again.';
      return;
    }

    const seekerUserPayload = {
      email: this.userForm.email,
      first_name: this.userForm.first_name,
      last_name: this.userForm.last_name,
    };

    const resumeRequest = this.resumeId
      ? this.resumeService.updateMyResume(this.resumeForm)
      : this.resumeService.createResume(this.resumeForm);

    forkJoin({
      user: this.auth.updateMe(seekerUserPayload),
      resume: resumeRequest,
    })
      .pipe(switchMap(() => this.auth.fetchMe()))
      .subscribe({
        next: (updatedUser) => {
          this.loading = false;
          this.resumeId = updatedUser.seeker_profile?.resume?.id ?? null;
          this.success = 'Profile updated successfully.';
          this.router.navigate(['/profile']);
        },
        error: () => {
          this.loading = false;
          this.error = 'Could not update the profile.';
        },
      });
  }

  addSkill(): void {
    if (!this.resumeId || !this.skillForm.name.trim()) {
      return;
    }

    this.resumeService.addSkill(this.resumeId, this.skillForm).pipe(
      switchMap(() => this.auth.fetchMe()),
    ).subscribe({
      next: (updatedUser) => {
        this.resumeId = updatedUser.seeker_profile?.resume?.id ?? null;
        this.skillForm = {
          name: '',
          level: 1,
        };
      },
      error: () => {
        this.error = 'Could not add skill.';
      },
    });
  }

  deleteSkill(skillId: number): void {
    this.resumeService.deleteSkill(skillId).pipe(
      switchMap(() => this.auth.fetchMe()),
    ).subscribe({
      next: (updatedUser) => {
        this.resumeId = updatedUser.seeker_profile?.resume?.id ?? null;
      },
      error: () => {
        this.error = 'Could not delete skill.';
      },
    });
  }

  addLanguage(): void {
    if (!this.resumeId || !this.languageForm.name.trim()) {
      return;
    }

    this.resumeService.addLanguage(this.resumeId, this.languageForm).pipe(
      switchMap(() => this.auth.fetchMe()),
    ).subscribe({
      next: (updatedUser) => {
        this.resumeId = updatedUser.seeker_profile?.resume?.id ?? null;
        this.languageForm = {
          name: '',
          level: 'beginner',
        };
      },
      error: () => {
        this.error = 'Could not add language.';
      },
    });
  }

  deleteLanguage(languageId: number): void {
    this.resumeService.deleteLanguage(languageId).pipe(
      switchMap(() => this.auth.fetchMe()),
    ).subscribe({
      next: (updatedUser) => {
        this.resumeId = updatedUser.seeker_profile?.resume?.id ?? null;
      },
      error: () => {
        this.error = 'Could not delete language.';
      },
    });
  }

  addExperience(): void {
    if (
      !this.resumeId ||
      !this.experienceForm.job_title.trim() ||
      !this.experienceForm.company.trim() ||
      !this.experienceForm.start_date ||
      !this.experienceForm.description.trim()
    ) {
      return;
    }

    this.resumeService.addExperience(this.resumeId, this.experienceForm).pipe(
      switchMap(() => this.auth.fetchMe()),
    ).subscribe({
      next: (updatedUser) => {
        this.resumeId = updatedUser.seeker_profile?.resume?.id ?? null;
        this.experienceForm = {
          job_title: '',
          company: '',
          start_date: '',
          end_date: '',
          description: '',
        };
      },
      error: () => {
        this.error = 'Could not add experience.';
      },
    });
  }

  deleteExperience(experienceId: number): void {
    this.resumeService.deleteExperience(experienceId).pipe(
      switchMap(() => this.auth.fetchMe()),
    ).subscribe({
      next: (updatedUser) => {
        this.resumeId = updatedUser.seeker_profile?.resume?.id ?? null;
      },
      error: () => {
        this.error = 'Could not delete experience.';
      },
    });
  }

  addEducation(): void {
    if (
      !this.resumeId ||
      !this.educationForm.institution.trim() ||
      !this.educationForm.degree.trim() ||
      !this.educationForm.start_date
    ) {
      return;
    }

    this.resumeService.addEducation(this.resumeId, this.educationForm).pipe(
      switchMap(() => this.auth.fetchMe()),
    ).subscribe({
      next: (updatedUser) => {
        this.resumeId = updatedUser.seeker_profile?.resume?.id ?? null;
        this.educationForm = {
          institution: '',
          degree: '',
          start_date: '',
          end_date: '',
        };
      },
      error: () => {
        this.error = 'Could not add education.';
      },
    });
  }

  deleteEducation(educationId: number): void {
    this.resumeService.deleteEducation(educationId).pipe(
      switchMap(() => this.auth.fetchMe()),
    ).subscribe({
      next: (updatedUser) => {
        this.resumeId = updatedUser.seeker_profile?.resume?.id ?? null;
      },
      error: () => {
        this.error = 'Could not delete education.';
      },
    });
  }

  private patchResumeForm(resume: Resume): void {
    this.resumeForm = {
      full_name: resume.full_name ?? '',
      location: resume.location ?? '',
      phone: resume.phone ?? '',
      photo: null,
      bio: resume.bio ?? '',
      availability: resume.availability ?? '',
      mobility: resume.mobility ?? false,
    };
  }
}