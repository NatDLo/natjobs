"""
Serializers for registration, profile retrieval, and profile updates.
"""

from rest_framework import serializers
from resumes.models import Resume
from resumes.serializers import ResumeSerializer
from .models import RecruiterProfile, SeekerProfile, User


class SeekerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for job seeker profiles, including nested resume data.
    The resume field is read-only and retrieves the associated Resume object for the seeker.
    """

    resume = serializers.SerializerMethodField()

    class Meta:
        model = SeekerProfile
        fields = [
            "resume",
        ]

    def get_resume(self, obj):
        try:
            resume = Resume.objects.get(user=obj.user)
        except Resume.DoesNotExist:
            return None

        return ResumeSerializer(resume, context=self.context).data


class RecruiterProfileSerializer(serializers.ModelSerializer):
    """Serializer for recruiter profiles, including the company name.
    The company_name field is editable for recruiters and read-only for job seekers.
    """ 
    
    class Meta:
        model = RecruiterProfile
        fields = [
            "company_name",
        ]


class UserPublicProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for public user profiles, including nested seeker and recruiter profiles.
    The seeker_profile and recruiter_profile fields are read-only and conditionally included based on the user's role.
    """

    seeker_profile = serializers.SerializerMethodField()
    recruiter_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "role",
            "seeker_profile",
            "recruiter_profile",
        ]

    def get_seeker_profile(self, obj):
        if obj.role != "seeker" or not hasattr(obj, "seekerprofile"):
            return None
        return SeekerProfileSerializer(obj.seekerprofile, context=self.context).data

    def get_recruiter_profile(self, obj):
        if obj.role != "recruiter" or not hasattr(obj, "recruiterprofile"):
            return None
        return RecruiterProfileSerializer(obj.recruiterprofile, context=self.context).data


class UserMeSerializer(UserPublicProfileSerializer):
    """
    Serializer for the authenticated user's own profile, including email.
    Inherits from UserPublicProfileSerializer and adds the email field, which is only visible to the user themselves.
    """

    class Meta(UserPublicProfileSerializer.Meta):
        fields = UserPublicProfileSerializer.Meta.fields + [
            "email",
        ]


class UserMeUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the authenticated user's profile information.
    Allows updates to first_name, last_name, and company_name (for recruiters).
    The company_name field is only editable for recruiters and is ignored for job seekers.
    """
    company_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "company_name",
        ]

    def validate(self, attrs):
        """Ensure that only recruiters can update the company_name field."""

        user = self.instance

        if user.role == "seeker" and "company_name" in attrs:
            raise serializers.ValidationError({
                "company_name": "Only recruiters can update company_name."
            })

        return attrs

    def update(self, instance, validated_data):
        """Update the user's profile information, including the company name for recruiters."""

        company_name = validated_data.pop("company_name", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if instance.role == "recruiter":
            profile, _ = RecruiterProfile.objects.get_or_create(
                user=instance,
                defaults={"company_name": ""},
            )
            if company_name is not None:
                profile.company_name = company_name
                profile.save()

        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration, including password handling.
    The password field is write-only and is used to create a new user with the specified role (recruiter or seeker).
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
        ]
        extra_kwargs = {
            "email": {"required": True, "allow_blank": False},
        }

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        """
        Create a new user with the provided registration data, including setting the password.
        The role field determines whether the user is a recruiter or a job seeker.
        """

        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data["role"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
