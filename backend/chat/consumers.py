import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.group_name = f"chat_{self.conversation_id}"

        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close(code=4001)
            return

        self.user = user

        conversation = await self.get_conversation_if_participant()
        if not conversation:
            await self.close(code=4003)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        messages = await self.get_last_messages()
        await self.send(text_data=json.dumps({"history": messages}))

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        content = (data.get("message") or "").strip()
        if not content:
            return

        await self.save_message(content)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": content,
                "sender": self.user.username,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "sender": event["sender"],
                }
            )
        )

    @database_sync_to_async
    def get_conversation_if_participant(self):
        try:
            conv = Conversation.objects.select_related("recruiter", "seeker").get(
                id=self.conversation_id
            )
        except Conversation.DoesNotExist:
            return None

        if self.user.id not in (conv.recruiter_id, conv.seeker_id):
            return None

        return conv

    @database_sync_to_async
    def get_last_messages(self):
        qs = (
            Message.objects.filter(conversation_id=self.conversation_id)
            .select_related("sender")
            .order_by("created_at")[:50]
        )

        return [
            {
                "sender": m.sender.username,
                "content": m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in qs
        ]

    @database_sync_to_async
    def save_message(self, content):
        return Message.objects.create(
            conversation_id=self.conversation_id,
            sender=self.user,
            content=content,
        )