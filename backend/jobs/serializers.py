"""Serialization rules for job CRUD payloads."""

from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for the Job model, used for creating, updating, and retrieving job postings.
    """
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['recruiter', 'created_at']