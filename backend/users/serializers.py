from rest_framework import serializers
from resumes.models import Resume
from resumes.serializers import ResumeSerializer
from .models import RecruiterProfile, SeekerProfile, User


class SeekerProfileSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = RecruiterProfile
        fields = [
            "company_name",
        ]


class UserPublicProfileSerializer(serializers.ModelSerializer):
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
    class Meta(UserPublicProfileSerializer.Meta):
        fields = UserPublicProfileSerializer.Meta.fields + [
            "email",
        ]


class UserMeUpdateSerializer(serializers.ModelSerializer):
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
        user = self.instance

        if user.role == "seeker" and "company_name" in attrs:
            raise serializers.ValidationError({
                "company_name": "Only recruiters can update company_name."
            })

        return attrs

    def update(self, instance, validated_data):
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

    def create(self, validated_data):
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