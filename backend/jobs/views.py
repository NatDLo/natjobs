"""
Job endpoints with role-aware querysets and recruiter-only mutations.
"""

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from applications.models import Application
from applications.serializers import ApplicationSerializer
from .models import Job
from .permissions import IsRecruiter
from .serializers import JobSerializer


class JobListCreateView(generics.ListCreateAPIView):
    """
    This view handles listing and creating job postings.
    GET: List all open jobs for candidates, or all jobs for recruiters.
    POST: Create a new job posting (recruiter-only).
    """

    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return open jobs for candidates, or all jobs for recruiters.
        """

        user = self.request.user

        if user.role == "recruiter":
            return Job.objects.filter(recruiter=user)

        return Job.objects.filter(status="open")

    def perform_create(self, serializer):
        """
        Ensure only recruiters can create jobs, and set the recruiter field to the current user.
        :var serializer: The serializer instance for the job being created.
        """

        if self.request.user.role != "recruiter":
            raise PermissionDenied("Only recruiters can create jobs.")

        serializer.save(recruiter=self.request.user)


class JobDetailView(generics.RetrieveAPIView):
    """
    This view handles retrieving a single job posting.
    GET: Retrieve a job posting by ID.
    """
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return open jobs for candidates, or all jobs for recruiters.
        """
        
        user = self.request.user

        if user.role == "recruiter":
            return Job.objects.filter(recruiter=user)

        return Job.objects.filter(status="open")


class JobUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view handles updating and deleting a job posting.
    GET: Retrieve a job posting by ID.
    PUT: Update a job posting (recruiter-only).
    DELETE: Delete a job posting (recruiter-only).
    """

    serializer_class = JobSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        """
        Return jobs for the current recruiter.
        """

        return Job.objects.filter(recruiter=self.request.user)


class JobApplicationsView(generics.ListAPIView):
    """
    This view handles listing applications for a specific job.
    GET: List all applications for a job (recruiter-only).
    """

    serializer_class = ApplicationSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        """
        Return applications for the specified job, ensuring the job belongs to the current recruiter.
        """
        
        job_id = self.kwargs["job_id"]
        return Application.objects.filter(
            job_id=job_id,
            job__recruiter=self.request.user,
        )
