export type UserRole = 'seeker' | 'recruiter';

export interface Skill {
  id: number;
  name: string;
  level: number;
}

export interface Language {
  id: number;
  name: string;
  level: string;
}

export interface Experience {
  id: number;
  job_title: string;
  company: string;
  start_date: string;
  end_date: string | null;
  description: string;
}

export interface Education {
  id: number;
  institution: string;
  degree: string;
  start_date: string;
  end_date: string | null;
}

export interface Resume {
  id: number;
  user: number;
  full_name: string;
  location: string;
  phone: string;
  photo: string | null;
  bio: string;
  availability: string;
  mobility: boolean;
  skills: Skill[];
  languages: Language[];
  experiences: Experience[];
  education: Education[];
}

export interface SeekerProfile {
  resume: Resume | null;
}

export interface RecruiterProfile {
  company_name: string;
}

export interface User {
  id: number;
  username: string;
  email?: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  seeker_profile: SeekerProfile | null;
  recruiter_profile: RecruiterProfile | null;
}

export interface LoginDto {
  username: string;
  password: string;
}

export interface RegisterDto {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  role: UserRole;
}

export interface UpdateMeDto {
  email?: string;
  first_name?: string;
  last_name?: string;
  company_name?: string;
}

export interface UpdateResumeDto {
  full_name?: string;
  location?: string;
  phone?: string;
  photo?: File | null;
  bio?: string;
  availability?: string;
  mobility?: boolean;
}

export interface CreateSkillDto {
  name: string;
  level: number;
}

export interface CreateLanguageDto {
  name: string;
  level: string;
}

export interface CreateExperienceDto {
  job_title: string;
  company: string;
  start_date: string;
  end_date?: string | null;
  description: string;
}

export interface CreateEducationDto {
  institution: string;
  degree: string;
  start_date: string;
  end_date?: string | null;
}

export interface TokenResponse {
  access: string;
  refresh: string;
}