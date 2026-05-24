import { Component, inject, NgZone, OnDestroy } from '@angular/core';
import { ChatService } from '../../../../core/services/chat.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-chat-widget',
  templateUrl: './chat-widget.html',
  styleUrls: ['./chat-widget.css'],
  standalone: true,
  imports: [FormsModule, CommonModule]
})

export class ChatWidgetComponent {
  private readonly chat = inject(ChatService);
  private readonly zone = inject(NgZone);

  open = false;
  conversations: any[] = [];
  messages: any[] = [];
  active: any = null;
  ws: WebSocket | null = null;
  wsConnected = false;
  wsError = '';
  message = '';

  toggle() {
    this.open = !this.open;

    if (!this.open) {
      this.cleanupSocket();
      this.active = null;
      this.messages = [];
      this.wsError = '';
      return;
    }

    this.chat.getConversations().subscribe({
      next: (res: any) => {
        this.conversations = Array.isArray(res) ? res : [];
      },
      error: () => {
        this.wsError = 'Could not load conversations.';
      },
    });
  }

  openConv(c: any) {
    this.active = c;
    this.messages = [];
    this.wsError = '';

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

  send() {
    if (!this.ws || !this.wsConnected || !this.message.trim()) return;

    this.ws.send(JSON.stringify({ message: this.message }));
    this.message = '';
  }

  ngOnDestroy(): void {
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