import { Component, inject, NgZone, OnDestroy, OnInit } from '@angular/core';
import { ChatService } from '../../../../core/services/chat.service';
import { AuthService } from '../../../../core/services/auth.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-chat-widget',
  templateUrl: './chat-widget.html',
  styleUrls: ['./chat-widget.css'],
  standalone: true,
  imports: [FormsModule, CommonModule],
})
export class ChatWidgetComponent implements OnInit, OnDestroy {
  private readonly chat = inject(ChatService);
  private readonly auth = inject(AuthService);
  private readonly zone = inject(NgZone);

  readonly currentUser = this.auth.user;

  open = false;
  conversations: any[] = [];
  messages: any[] = [];
  active: any = null;
  ws: WebSocket | null = null;
  wsConnected = false;
  wsError = '';
  message = '';
  totalUnread = 0;
  private pollInterval: any = null;

  ngOnInit(): void {
    this.refreshConversations();
    // Poll unread status periodically
    this.pollInterval = setInterval(() => {
      this.refreshConversations();
    }, 15000);
  }

  refreshConversations(): void {
    this.chat.getConversations().subscribe({
      next: (res: any) => {
        this.conversations = Array.isArray(res) ? res : [];
        this.recalculateUnread();
      },
      error: () => {
        // Silent fail on background refresh
      },
    });
  }

  recalculateUnread(): void {
    this.totalUnread = this.conversations.reduce(
      (sum, c) => sum + (c.unread_count || 0),
      0,
    );
  }

  getContactName(c: any): string {
    if (!c) return 'Conversation';
    if (c.other_user?.username) {
      const company = c.other_user.company_name
        ? ` (${c.other_user.company_name})`
        : '';
      return `${c.other_user.username}${company}`;
    }
    const current = this.currentUser();
    if (current && current.role === 'recruiter' && c.seeker_username) {
      return c.seeker_username;
    }
    if (current && current.role === 'seeker' && c.recruiter_username) {
      return c.recruiter_username;
    }
    return `Chat #${c.id}`;
  }

  getContactRole(c: any): string {
    if (!c?.other_user?.role) return '';
    return c.other_user.role === 'recruiter' ? 'Recruiter' : 'Seeker';
  }

  toggle(): void {
    this.open = !this.open;

    if (!this.open) {
      this.cleanupSocket();
      this.active = null;
      this.messages = [];
      this.wsError = '';
      return;
    }

    this.refreshConversations();
  }

  openConv(c: any): void {
    this.active = c;
    this.messages = [];
    this.wsError = '';

    if (c.unread_count > 0) {
      this.chat.markAsRead(c.id).subscribe({
        next: () => {
          c.unread_count = 0;
          this.recalculateUnread();
        },
      });
    }

    this.cleanupSocket();
    this.ws = this.chat.connect(c.id);

    if (!this.ws) return;

    this.ws.onopen = () => {
      this.zone.run(() => {
        this.wsConnected = true;
        this.wsError = '';
      });
    };

    this.ws.onmessage = (e) => {
      let data: any;

      try {
        data = JSON.parse(e.data);
      } catch {
        return;
      }

      this.zone.run(() => {
        if (Array.isArray(data.history)) {
          this.messages = data.history
            .map((item: any) => this.normalizeMessage(item))
            .filter((item: any) => !!item);
          return;
        }

        const normalized = this.normalizeMessage(data);
        if (!normalized) {
          return;
        }

        this.messages = [...this.messages, normalized];

        // Update last message preview
        if (this.active) {
          this.active.last_message = {
            content: normalized.content,
            sender: normalized.sender,
            created_at: normalized.created_at || new Date().toISOString(),
          };
        }

        // If incoming message is from someone else while conversation is active, mark read
        const current = this.currentUser();
        if (current && normalized.sender !== current.username && this.active?.id === c.id) {
          this.chat.markAsRead(c.id).subscribe();
        }
      });
    };

    this.ws.onerror = () => {
      this.zone.run(() => {
        this.wsError = 'WebSocket connection failed. Start backend with ASGI support.';
      });
    };

    this.ws.onclose = () => {
      this.zone.run(() => {
        this.wsConnected = false;
      });
    };
  }

  send(): void {
    if (!this.ws || !this.wsConnected || !this.message.trim()) return;

    this.ws.send(JSON.stringify({ message: this.message }));
    this.message = '';
  }

  ngOnDestroy(): void {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
    }
    this.cleanupSocket();
  }

  private cleanupSocket(): void {
    if (!this.ws) {
      this.wsConnected = false;
      return;
    }

    this.ws.onopen = null;
    this.ws.onmessage = null;
    this.ws.onerror = null;
    this.ws.onclose = null;
    this.ws.close();
    this.ws = null;
    this.wsConnected = false;
  }

  private normalizeMessage(raw: any): { sender: string; content: string; created_at?: string } | null {
    const sender = typeof raw?.sender === 'string' ? raw.sender : 'Unknown';
    const content =
      typeof raw?.content === 'string'
        ? raw.content
        : typeof raw?.message === 'string'
          ? raw.message
          : '';

    if (!content.trim()) {
      return null;
    }

    return {
      sender,
      content,
      created_at: typeof raw?.created_at === 'string' ? raw.created_at : undefined,
    };
  }
}