import { HttpClient } from "@angular/common/http";
import { inject, Injectable } from "@angular/core";
import { buildWsUrl } from "../config/api-config";

@Injectable({ providedIn: "root" })
export class ChatService {
  private http = inject(HttpClient);

  getConversations() {
    return this.http.get<any[]>("/api/chat/conversations/");
  }

  getUnreadCount() {
    return this.http.get<{ unread_count: number }>("/api/chat/unread-count/");
  }

  markAsRead(conversationId: number) {
    return this.http.post(`/api/chat/conversations/${conversationId}/read/`, {});
  }

  createConversation(data: any) {
    return this.http.post("/api/chat/conversations/create/", data);
  }

  connect(id: number) {
    const token = localStorage.getItem("token");
    const wsUrl = buildWsUrl(`/ws/chat/${id}/`, token);
    return new WebSocket(wsUrl);
  }
}