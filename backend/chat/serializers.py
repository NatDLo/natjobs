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

    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ['created_at']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for message objects.
    Allows specifying sender ID and conversation ID for creation.
    """
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'created_at']