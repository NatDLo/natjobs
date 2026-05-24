"""
Application serializers for creation/listing and recruiter status updates.
Includes nested job details for application listing and separate serializer for updating 
application status by recruiters.
"""

from rest_framework import serializers
from .models import Application


class ApplicationJobSerializer(serializers.Serializer):
    """
    Serializer for nested job details in application listing.
    Includes job ID, title, and recruiter ID for reference in application responses.
    """

    id = serializers.IntegerField()
    title = serializers.CharField()
    recruiter = serializers.IntegerField(source="recruiter_id")


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and listing job applications.
    Includes nested job details and allows specifying job ID for creation.
    """
    
    job = ApplicationJobSerializer(read_only=True)
    job_id = serializers.IntegerField(write_only=True, source="job")

    class Meta:
        model = Application
        fields = [
            "id",
            "seeker",
            "job",
            "job_id",
            "resume",
            "applied_at",
            "status",
            "notes",
        ]
        read_only_fields = [
            "seeker",
            "job",
            "resume",
            "applied_at",
        ]


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the status and notes of a job application.
    Used by recruiters to manage the application process.
    """
    
    class Meta:
        model = Application
        fields = [
            "status",
            "notes",
        ]