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