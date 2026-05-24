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
      error: () => {
        this.loading = false;
        this.error = 'Could not create the account.';
      },
    });
  }
}