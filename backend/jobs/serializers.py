"""Serialization rules for job CRUD payloads."""

from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for the Job model, used for creating, updating, and retrieving job postings.
    """
    recruiter_username = serializers.CharField(source="recruiter.username", read_only=True)
    has_applied = serializers.SerializerMethodField()
    application_status = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            "id",
            "recruiter",
            "recruiter_username",
            "title",
            "description",
            "location",
            "status",
            "created_at",
            "has_applied",
            "application_status",
        ]
        read_only_fields = ["recruiter", "created_at"]

    def get_has_applied(self, obj):
        """
        Check if the current authenticated seeker has already applied to this job.

        :param obj: The Job model instance.
        :return: True if the authenticated seeker applied, False otherwise.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated and request.user.role == "seeker":
            return obj.applications.filter(seeker=request.user).exists()
        return False

    def get_application_status(self, obj):
        """
        Retrieve the application status string for the current authenticated seeker.

        :param obj: The Job model instance.
        :return: Application status string or None if not applied.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated and request.user.role == "seeker":
            app = obj.applications.filter(seeker=request.user).first()
            return app.status if app else None
        return None