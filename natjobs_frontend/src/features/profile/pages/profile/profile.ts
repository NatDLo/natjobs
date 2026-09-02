import { Component, inject, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './profile.html',
  styleUrls: ['./profile.css'],
})
export class Profile implements OnInit {
  private readonly auth = inject(AuthService);

  readonly user = this.auth.user;

  ngOnInit(): void {
    this.auth.fetchMe().subscribe();
  }
}