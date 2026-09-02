"""
Serializers for conversation and message transport.
"""

from rest_framework import serializers
from .models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for conversation objects.
    Includes nested messages and allows specifying recruiter and seeker IDs for creation.
    """
    recruiter_username = serializers.CharField(source="recruiter.username", read_only=True)
    seeker_username = serializers.CharField(source="seeker.username", read_only=True)
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "recruiter",
            "seeker",
            "recruiter_username",
            "seeker_username",
            "other_user",
            "last_message",
            "unread_count",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def get_other_user(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None
        current_user = request.user
        other = obj.seeker if current_user.id == obj.recruiter_id else obj.recruiter

        company = ""
        if hasattr(other, "recruiterprofile") and other.recruiterprofile:
            company = other.recruiterprofile.company_name

        return {
            "id": other.id,
            "username": other.username,
            "role": getattr(other, "role", ""),
            "company_name": company,
        }

    def get_last_message(self, obj):
        msg = obj.messages.order_by("-created_at").first()
        if not msg:
            return None
        return {
            "content": msg.content,
            "sender": msg.sender.username,
            "created_at": msg.created_at.isoformat(),
        }

    def get_unread_count(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return 0
        return obj.messages.filter(is_read=False).exclude(sender=request.user).count()


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for message objects.
    Allows specifying sender ID and conversation ID for creation.
    """
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "conversation", "sender", "sender_username", "content", "is_read", "created_at"]
        read_only_fields = ["sender", "created_at"]