"""
Conversation and message models for recruiter-seeker communication.
"""

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Conversation(models.Model):
    """
    Represents a conversation between a recruiter and a seeker.
    Each conversation is unique to a recruiter-seeker pair.
    """

    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recruiter_chats")
    seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seeker_chats")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("recruiter", "seeker")

    def __str__(self):
        return f"{self.recruiter} ↔ {self.seeker}"


class Message(models.Model):
    """
    Represents a message within a conversation between a recruiter and a seeker.
    """
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.content[:20]}"