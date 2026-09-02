import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';
import { RegisterDto } from '../../auth-module';

@Component({
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.html',
  styleUrls: ['./register.css'],
})
export class Register {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  form: RegisterDto = {
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    role: 'seeker',
  };

  loading = false;
  error = '';

  register(): void {
    if (!this.form.username.trim() || !this.form.email.trim() || !this.form.password.trim()) {
      this.error = 'Please complete username, email, and password.';
      return;
    }

    this.loading = true;
    this.error = '';

    this.auth.register(this.form).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/auth/login']);
      },
      error: (err) => {
        this.loading = false;
        this.error = this.parseErrorMessage(err);
      },
    });
  }

  private parseErrorMessage(err: any): string {
    const errorObj = err?.error;
    if (!errorObj) {
      return 'Could not create the account.';
    }

    if (typeof errorObj === 'string') {
      return errorObj;
    }

    if (errorObj.username) {
      const uErr = Array.isArray(errorObj.username) ? errorObj.username[0] : errorObj.username;
      return typeof uErr === 'string' ? uErr : 'This username is already in use.';
    }

    if (errorObj.email) {
      const eErr = Array.isArray(errorObj.email) ? errorObj.email[0] : errorObj.email;
      return typeof eErr === 'string' ? eErr : 'This email is already in use.';
    }

    if (errorObj.password) {
      const pErr = Array.isArray(errorObj.password) ? errorObj.password[0] : errorObj.password;
      return typeof pErr === 'string' ? pErr : 'Invalid password.';
    }

    if (errorObj.detail) {
      return typeof errorObj.detail === 'string' ? errorObj.detail : 'Could not create the account.';
    }

    const firstKey = Object.keys(errorObj)[0];
    if (firstKey) {
      const val = errorObj[firstKey];
      return Array.isArray(val) ? val[0] : String(val);
    }

    return 'Could not create the account.';
  }
}