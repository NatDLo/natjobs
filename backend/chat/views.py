"""
HTTP endpoints for listing, creating, and retrieving conversations.
Only authenticated users can access these endpoints, and they can only see conversations they are a part of.
"""

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Conversation
from .serializers import ConversationSerializer

User = get_user_model()


class ConversationListView(generics.ListAPIView):
    """
    View for listing all conversations for the authenticated user.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user

        return Conversation.objects.filter(
            recruiter=user
        ) | Conversation.objects.filter(
            seeker=user
        )


class ConversationCreateView(generics.CreateAPIView):
    """
    View for creating a new conversation between a recruiter and a seeker.
    The request must include recruiter and seeker IDs, and the authenticated user must be one of them.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation between a recruiter and a seeker.
        Validates that the recruiter and seeker exist and that the authenticated user is one of them.
        """

        recruiter_id = request.data.get("recruiter")
        seeker_id = request.data.get("seeker")

        if not recruiter_id or not seeker_id:
            raise ValidationError("recruiter and seeker are required")

        try:
            recruiter = User.objects.get(pk=recruiter_id, role="recruiter")
            seeker = User.objects.get(pk=seeker_id, role="seeker")
        except User.DoesNotExist:
            raise ValidationError("Invalid recruiter or seeker.")

        if request.user.id not in {recruiter.id, seeker.id}:
            raise PermissionDenied("You can only create conversations you participate in.")

        conversation, created = Conversation.objects.get_or_create(
            recruiter=recruiter,
            seeker=seeker,
        )

        serializer = self.get_serializer(conversation)
        return Response(serializer.data)


class ConversationDetailView(generics.RetrieveAPIView):
    """
    View for retrieving a specific conversation by ID.
    Only participants of the conversation can access it.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user

        return Conversation.objects.filter(
            recruiter=user
        ) | Conversation.objects.filter(
            seeker=user
        )