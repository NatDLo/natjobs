"""
Views for managing job applications.
"""

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError

from resumes.models import Resume
from jobs.permissions import IsRecruiter
from .models import Application
from .permissions import IsSeeker
from .serializers import ApplicationSerializer, ApplicationStatusUpdateSerializer


class ApplicationListCreateView(generics.ListCreateAPIView):
    """
    View to list and create job applications.
    GET: List all applications for the authenticated seeker.
    POST: Create a new application for a job.
    """

    serializer_class = ApplicationSerializer
    permission_classes = [IsSeeker]

    def get_queryset(self):
        """
        Return applications for the authenticated seeker.
        """

        return Application.objects.filter(seeker=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new application for a job.
        Ensure the job is open and the seeker has not already applied.
        """

        if self.request.user.role != "seeker":
            raise PermissionDenied("Only seekers can apply to jobs")

        job = serializer.validated_data["job"]

        if job.status != "open":
            raise ValidationError("This job is not open for applications.")

        if Application.objects.filter(seeker=self.request.user, job=job).exists():
            raise ValidationError("You already applied to this job.")

        try:
            resume = Resume.objects.get(user=self.request.user)
        except Resume.DoesNotExist:
            raise ValidationError(
                {"detail": "Create your resume before applying to a job."}
            )

        serializer.save(seeker=self.request.user, resume=resume)


class ApplicationDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a specific job application.
    GET: Retrieve details of a specific application for the authenticated user.
    """

    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return applications for the authenticated user.
        - Seekers can only see their own applications.
        - Recruiters can only see applications for their jobs.
        """

        user = self.request.user

        if user.role == "seeker":
            return Application.objects.filter(seeker=user)

        if user.role == "recruiter":
            return Application.objects.filter(job__recruiter=user)

        return Application.objects.none()


class ApplicationUpdateStatusView(generics.UpdateAPIView):
    """
    View to update the status of a job application.
    PATCH: Update the status of a specific application for the authenticated recruiter.
    """

    serializer_class = ApplicationStatusUpdateSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        """
        Return applications for the authenticated recruiter.
        Recruiters can only update applications for their jobs.
        """
        
        return Application.objects.filter(job__recruiter=self.request.user)

    def perform_update(self, serializer):
        """
        Update the application status and send a notification message in chat on any status change.

        :param serializer: ApplicationStatusUpdateSerializer instance.
        """
        prev_status = serializer.instance.status
        instance = serializer.save()
        new_status = instance.status

        if new_status != prev_status:
            try:
                from chat.models import Conversation, Message
                from asgiref.sync import async_to_sync
                from channels.layers import get_channel_layer

                conversation, _ = Conversation.objects.get_or_create(
                    recruiter=self.request.user,
                    seeker=instance.seeker,
                )

                if new_status == "accepted":
                    status_text = "accepted 🎉"
                elif new_status == "interview":
                    status_text = "moved to the Interview stage 📅"
                elif new_status == "reviewing":
                    status_text = "moved to Reviewing 🔍"
                elif new_status == "rejected":
                    status_text = "updated to Rejected"
                else:
                    status_text = f"updated to '{new_status}'"

                msg_text = (
                    f"Hello {instance.seeker.username}! Your application for '{instance.job.title}' "
                    f"has been {status_text} by {self.request.user.username}."
                )

                Message.objects.create(
                    conversation=conversation,
                    sender=self.request.user,
                    content=msg_text,
                    is_read=False,
                )

                channel_layer = get_channel_layer()
                if channel_layer:
                    async_to_sync(channel_layer.group_send)(
                        f"chat_{conversation.id}",
                        {
                            "type": "chat.message",
                            "conversation_id": conversation.id,
                            "message": msg_text,
                            "sender": self.request.user.username,
                        },
                    )
            except Exception:
                pass