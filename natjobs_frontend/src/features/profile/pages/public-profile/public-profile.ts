import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../../core/services/auth.service';
import { ChatService } from '../../../../core/services/chat.service';
import { User } from '../../../auth/auth-module';

@Component({
  selector: 'app-public-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './public-profile.html',
  styleUrls: ['./public-profile.css'],
})
export class PublicProfileComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly auth = inject(AuthService);
  private readonly chatService = inject(ChatService);

  readonly currentUser = this.auth.user;

  profileSignal = signal<User | null>(null);
  error = '';
  loading = true;
  startingChat = false;

  readonly canMessage = computed(() => {
    const me = this.currentUser();
    const other = this.profileSignal();
    if (!me || !other) return false;
    if (me.id === other.id) return false;
    return (
      (me.role === 'recruiter' && other.role === 'seeker') ||
      (me.role === 'seeker' && other.role === 'recruiter')
    );
  });

  get profile(): User | null {
    return this.profileSignal();
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      const id = Number(params.get('id'));

      if (!id) {
        this.loading = false;
        this.error = 'Invalid user profile.';
        return;
      }

      this.loading = true;
      this.error = '';

      this.auth.getPublicProfile(id).subscribe({
        next: (user) => {
          this.profileSignal.set(user);
          this.loading = false;
        },
        error: () => {
          this.error = 'Could not load this profile.';
          this.loading = false;
        },
      });
    });
  }

  sendMessage(): void {
    const me = this.currentUser();
    const other = this.profileSignal();

    if (!me || !other || this.startingChat) return;

    this.startingChat = true;

    this.chatService
      .createConversation({
        user_id: other.id,
      })
      .subscribe({
        next: () => {
          this.startingChat = false;
          alert(
            `Chat with ${other.username} is active! Open the chat widget (bottom right 💬) to message.`
          );
        },
        error: () => {
          this.startingChat = false;
          alert('Could not start conversation with this user.');
        },
      });
  }
}