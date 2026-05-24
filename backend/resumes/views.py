from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Resume, Skill, Language, Experience, Education
from .serializers import (
    ResumeSerializer,
    SkillSerializer,
    LanguageSerializer,
    ExperienceSerializer,
    EducationSerializer,
)


class SeekerOnlyMixin:
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.user.role != "seeker":
            raise PermissionDenied("Only seekers can manage resumes.")


class ResumeListCreateView(SeekerOnlyMixin, generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user).prefetch_related(
            "skills",
            "languages",
            "experiences",
            "education",
        )

    def perform_create(self, serializer):
        if Resume.objects.filter(user=self.request.user).exists():
            raise ValidationError({"detail": "You already have a resume."})

        serializer.save(user=self.request.user)


class ResumeMeView(SeekerOnlyMixin, generics.RetrieveUpdateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Resume.objects.prefetch_related(
                "skills",
                "languages",
                "experiences",
                "education",
            ),
            user=self.request.user,
        )


class ResumeDetailView(SeekerOnlyMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user).prefetch_related(
            "skills",
            "languages",
            "experiences",
            "education",
        )


class SkillListCreateView(SeekerOnlyMixin, generics.ListCreateAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_resume(self):
        return get_object_or_404(
            Resume,
            pk=self.kwargs["resume_id"],
            user=self.request.user,
        )

    def get_queryset(self):
        return Skill.objects.filter(resume=self.get_resume())

    def perform_create(self, serializer):
        serializer.save(resume=self.get_resume())


class SkillUpdateView(SeekerOnlyMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(resume__user=self.request.user)


class LanguageListCreateView(SeekerOnlyMixin, generics.ListCreateAPIView):
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_resume(self):
        return get_object_or_404(
            Resume,
            pk=self.kwargs["resume_id"],
            user=self.request.user,
        )

    def get_queryset(self):
        return Language.objects.filter(resume=self.get_resume())

    def perform_create(self, serializer):
        serializer.save(resume=self.get_resume())


class LanguageUpdateView(SeekerOnlyMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Language.objects.filter(resume__user=self.request.user)


class ExperienceListCreateView(SeekerOnlyMixin, generics.ListCreateAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_resume(self):
        return get_object_or_404(
            Resume,
            pk=self.kwargs["resume_id"],
            user=self.request.user,
        )

    def get_queryset(self):
        return Experience.objects.filter(resume=self.get_resume())

    def perform_create(self, serializer):
        serializer.save(resume=self.get_resume())


class ExperienceUpdateView(SeekerOnlyMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Experience.objects.filter(resume__user=self.request.user)


class EducationListCreateView(SeekerOnlyMixin, generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_resume(self):
        return get_object_or_404(
            Resume,
            pk=self.kwargs["resume_id"],
            user=self.request.user,
        )

    def get_queryset(self):
        return Education.objects.filter(resume=self.get_resume())

    def perform_create(self, serializer):
        serializer.save(resume=self.get_resume())


class EducationUpdateView(SeekerOnlyMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Education.objects.filter(resume__user=self.request.user)