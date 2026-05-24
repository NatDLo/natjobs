import { Component, inject } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { ChatWidgetComponent } from '../../features/chat/components/chat-widget/chat-widget';
import { AuthService } from '../../core/services/auth.service';
import { NavbarComponent } from '../navbar/navbar';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, ChatWidgetComponent],
  templateUrl: './main-layout.html',
  styleUrls: ['./main-layout.css'],
})
export class MainLayoutComponent {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  readonly user = this.auth.user;
  readonly isAuthed = this.auth.isAuthenticated;

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/auth/login']);
  }
}