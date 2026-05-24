from rest_framework import serializers
from .models import Application


class ApplicationJobSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    recruiter = serializers.IntegerField(source="recruiter_id")


class ApplicationSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Application
        fields = [
            "status",
            "notes",
        ]