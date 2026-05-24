import { computed, inject, Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, of, switchMap, tap } from 'rxjs';
import { API_BASE_URL } from '../config/api-config';
import {
  LoginDto,
  RegisterDto,
  TokenResponse,
  UpdateMeDto,
  User,
  UserRole,
} from '../../features/auth/auth-module';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly tokenKey = 'token';
  private readonly refreshKey = 'refresh';
  private readonly userSignal = signal<User | null>(null);

  readonly user = this.userSignal.asReadonly();
  readonly isAuthenticated = computed(() => !!this.token());
  readonly role = computed<UserRole | null>(() => this.userSignal()?.role ?? null);

  login(data: LoginDto): Observable<User> {
    return this.http.post<TokenResponse>(`${API_BASE_URL}/login/`, data).pipe(
      tap((tokens) => this.persistTokens(tokens)),
      switchMap(() => this.fetchMe()),
    );
  }

  register(data: RegisterDto): Observable<User> {
    return this.http.post<User>(`${API_BASE_URL}/users/register/`, data);
  }

  fetchMe(): Observable<User> {
    return this.http.get<User>(`${API_BASE_URL}/users/me/`).pipe(
      tap((user) => this.userSignal.set(user)),
    );
  }

  updateMe(data: UpdateMeDto): Observable<User> {
    return this.http.patch<User>(`${API_BASE_URL}/users/me/`, data).pipe(
      tap((user) => this.userSignal.set(user)),
    );
  }

  getPublicProfile(id: number): Observable<User> {
    return this.http.get<User>(`${API_BASE_URL}/users/${id}/`);
  }

  restoreSession(): Observable<User | null> {
    if (!this.token()) {
      this.userSignal.set(null);
      return of(null);
    }

    return this.fetchMe().pipe(
      catchError(() => {
        this.logout();
        return of(null);
      }),
    );
  }

  token(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  refreshToken(): string | null {
    return localStorage.getItem(this.refreshKey);
  }

  hasRole(role: UserRole): boolean {
    return this.userSignal()?.role === role;
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.refreshKey);
    this.userSignal.set(null);
  }

  private persistTokens(tokens: TokenResponse): void {
    localStorage.setItem(this.tokenKey, tokens.access);
    localStorage.setItem(this.refreshKey, tokens.refresh);
  }
}