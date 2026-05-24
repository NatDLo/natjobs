"""
Async WebSocket consumer for authenticated, participant-scoped real-time chat.
This consumer handles WebSocket connections for chat conversations, ensuring that only authenticated users
who are participants in the conversation can connect and exchange messages in real time.
"""

import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling chat messages in real-time.
    Ensures that only authenticated users who are participants in the conversation can connect.
    """

    async def connect(self):
        """
        Handle a new WebSocket connection.
        Validates the user's authentication and conversation participation before accepting the connection.
        If the user is not authenticated or not a participant in the conversation, the connection is rejected
        with appropriate close codes.
        """

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
        """
        Handle WebSocket disconnection.
        Removes the connection from the conversation group to stop receiving messages.
        """

        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Handle incoming WebSocket messages.
        Validates the message content and saves it to the database before broadcasting it to the conversation group
        for real-time delivery to all participants.
        """

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
        """
        Handle a chat message event.
        Sends the message to the WebSocket client.
        """

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
        """
        Retrieve the conversation if the user is a participant (recruiter or seeker).
        Returns the conversation object if the user is a participant, otherwise returns None.
        """

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
        """
        Retrieve the last 50 messages for the conversation.
        Returns a list of message dictionaries containing the sender, content, and creation timestamp.
        """

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
        """
        Save a new message to the database for the conversation.
        Creates a new Message object with the conversation ID, sender, and content.
        """
        
        return Message.objects.create(
            conversation_id=self.conversation_id,
            sender=self.user,
            content=content,
        )