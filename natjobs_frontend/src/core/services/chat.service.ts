import { HttpClient } from "@angular/common/http";
import { inject, Injectable } from "@angular/core";
import { buildWsUrl } from "../config/api-config";

@Injectable({ providedIn: "root" })
export class ChatService {
  private http = inject(HttpClient);

  getConversations() {
    return this.http.get("/api/chat/conversations/");
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