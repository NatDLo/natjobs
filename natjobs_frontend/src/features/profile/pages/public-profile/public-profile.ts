import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';
import { User } from '../../../auth/auth-module';

@Component({
  selector: 'app-public-profile',
  standalone: true,
  imports: [],
  templateUrl: './public-profile.html',
  styleUrls: ['./public-profile.css'],
})
export class PublicProfileComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly auth = inject(AuthService);

  profile: User | null = null;
  error = '';
  loading = true;

  constructor() {
    const id = Number(this.route.snapshot.params['id']);

    if (!id) {
      this.loading = false;
      this.error = 'Invalid user profile.';
      return;
    }

    this.auth.getPublicProfile(id).subscribe({
      next: (user) => {
        this.profile = user;
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not load this profile.';
        this.loading = false;
      },
    });
  }
}