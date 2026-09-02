"""
HTTP endpoints for listing, creating, and retrieving conversations.
Only authenticated users can access these endpoints, and they can only see conversations they are a part of.
"""

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Conversation, Message
from .serializers import ConversationSerializer

User = get_user_model()


class ConversationListView(generics.ListAPIView):
    """
    View for listing all conversations for the authenticated user.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        """
        Return conversations where the authenticated user is either the recruiter or the seeker.
        """
        user = self.request.user

        return (
            Conversation.objects.filter(Q(recruiter=user) | Q(seeker=user))
            .select_related("recruiter", "seeker")
            .prefetch_related("messages", "recruiter__recruiterprofile", "seeker__seekerprofile")
            .distinct()
            .order_by("-created_at")
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
        Supports passing either `user_id` / `other_user_id` or explicit `recruiter` and `seeker`.
        """

        other_user_id = request.data.get("user_id") or request.data.get("other_user_id")

        if other_user_id:
            try:
                other_user = User.objects.get(pk=other_user_id)
            except User.DoesNotExist:
                raise ValidationError("Target user not found.")

            if request.user.role == "recruiter" and other_user.role == "seeker":
                recruiter = request.user
                seeker = other_user
            elif request.user.role == "seeker" and other_user.role == "recruiter":
                seeker = request.user
                recruiter = other_user
            else:
                raise ValidationError("Conversations must be between a recruiter and a job seeker.")
        else:
            recruiter_id = request.data.get("recruiter")
            seeker_id = request.data.get("seeker")

            if not recruiter_id or not seeker_id:
                raise ValidationError("recruiter and seeker (or user_id) are required.")

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

        serializer = self.get_serializer(conversation, context=self.get_serializer_context())
        return Response(serializer.data)


class ConversationDetailView(generics.RetrieveAPIView):
    """
    View for retrieving a specific conversation by ID.
    Only participants of the conversation can access it.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        """
        Return conversations where the authenticated user is either the recruiter or the seeker.
        """

        user = self.request.user

        return Conversation.objects.filter(Q(recruiter=user) | Q(seeker=user))


class MarkConversationReadView(generics.GenericAPIView):
    """
    Mark all unread incoming messages in a conversation as read.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """
        Mark all messages sent by the other party in this conversation as read.

        :param request: The incoming HTTP request.
        :param pk: Conversation ID.
        :return: Response with status 'ok'.
        """
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation not found.")

        if request.user.id not in (conversation.recruiter_id, conversation.seeker_id):
            raise PermissionDenied("Not a participant in this conversation.")

        Message.objects.filter(conversation=conversation, is_read=False).exclude(sender=request.user).update(is_read=True)
        return Response({"status": "ok"})


class UnreadCountView(generics.GenericAPIView):
    """
    Returns the total unread message count for the current authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Calculate total unread messages across all conversations of the authenticated user.

        :param request: The incoming HTTP request.
        :return: Response containing 'unread_count' integer.
        """
        user = request.user
        unread_total = Message.objects.filter(
            conversation__in=Conversation.objects.filter(Q(recruiter=user) | Q(seeker=user)),
            is_read=False,
        ).exclude(sender=user).count()
        return Response({"unread_count": unread_total})