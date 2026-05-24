import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';
import { LoginDto } from '../../auth-module';

@Component({
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css'],
})
export class Login {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  form: LoginDto = {
    username: '',
    password: '',
  };

  loading = false;
  error = '';

  login(): void {
    if (!this.form.username.trim() || !this.form.password.trim()) {
      this.error = 'Please enter your username and password.';
      return;
    }

    this.loading = true;
    this.error = '';

    this.auth.login(this.form).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigateByUrl('/');
      },
      error: () => {
        this.loading = false;
        this.error = 'Invalid username or password.';
      },
    });
  }
}