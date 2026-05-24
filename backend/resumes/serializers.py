"""
Serializers for resume aggregate and nested resume entities.
Nesteed fields are read-only and managed via separate endpoints for skills, languages, experience, and education.
"""

from rest_framework import serializers
from .models import Resume, Skill, Language, Experience, Education


class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer for a candidate's skill with proficiency level.
    """

    class Meta:
        model = Skill
        fields = [
            "id",
            "resume",
            "name",
            "level",
        ]
        read_only_fields = ["resume"]


class LanguageSerializer(serializers.ModelSerializer):
    """
    Serializer for a candidate's language proficiency.
    """
    
    class Meta:
        model = Language
        fields = [
            "id",
            "resume",
            "name",
            "level",
        ]
        read_only_fields = ["resume"]


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer for a candidate's work experience.
    """

    class Meta:
        model = Experience
        fields = [
            "id",
            "resume",
            "job_title",
            "company",
            "start_date",
            "end_date",
            "description",
        ]
        read_only_fields = ["resume"]


class EducationSerializer(serializers.ModelSerializer):
    """
    Serializer for a candidate's educational background.
    """

    class Meta:
        model = Education
        fields = [
            "id",
            "resume",
            "institution",
            "degree",
            "start_date",
            "end_date",
        ]
        read_only_fields = ["resume"]


class ResumeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Resume aggregate, including nested read-only fields for skills, languages, experience, and education.
    """

    skills = SkillSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = [
            "id",
            "user",
            "full_name",
            "location",
            "phone",
            "photo",
            "bio",
            "availability",
            "mobility",
            "skills",
            "languages",
            "experiences",
            "education",
        ]
        read_only_fields = [
            "user",
            "skills",
            "languages",
            "experiences",
            "education",
        ]