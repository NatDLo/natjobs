"""
WebSocket routing patterns for chat consumers.
Defines the URL patterns for WebSocket connections to the chat consumer, allowing real-time communication between users in a conversation.
"""

from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<conversation_id>[^/]+)/$", ChatConsumer.as_asgi()),
]