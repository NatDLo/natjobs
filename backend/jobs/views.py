from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from applications.models import Application
from applications.serializers import ApplicationSerializer
from .models import Job
from .permissions import IsRecruiter
from .serializers import JobSerializer


class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "recruiter":
            return Job.objects.filter(recruiter=user)

        return Job.objects.filter(status="open")

    def perform_create(self, serializer):
        if self.request.user.role != "recruiter":
            raise PermissionDenied("Only recruiters can create jobs.")

        serializer.save(recruiter=self.request.user)


class JobDetailView(generics.RetrieveAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "recruiter":
            return Job.objects.filter(recruiter=user)

        return Job.objects.filter(status="open")


class JobUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)


class JobApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        job_id = self.kwargs["job_id"]
        return Application.objects.filter(
            job_id=job_id,
            job__recruiter=self.request.user,
        )