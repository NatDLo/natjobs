"""
Seeker-only resume CRUD and nested resource management endpoints.
Shared role gate for all resume endpoints via SeekerOnlyMixin.
Prevent duplicate resumes per user in ResumeListCreateView.
Always scope resume and nested resource queries to the authenticated user to ensure data isolation and security.
"""

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
    """
    Mixin to restrict access to seekers only for resume-related views.
    """

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.user.role != "seeker":
            raise PermissionDenied("Only seekers can manage resumes.")


class ResumeListCreateView(SeekerOnlyMixin, generics.ListCreateAPIView):
    """
    List and create resume for the authenticated seeker.
    Each seeker can only have one resume, enforced in perform_create.
    """
    
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
    """
    Retrieve and update the authenticated seeker's resume.
    """
    
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
    """
    Retrieve, update, and delete the authenticated seeker's resume.
    """
    
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensure we only operate on the authenticated seeker's resume.
        """

        return Resume.objects.filter(user=self.request.user).prefetch_related(
            "skills",
            "languages",
            "experiences",
            "education",
        )


class SkillListCreateView(SeekerOnlyMixin, generics.ListCreateAPIView):
    """
    List and create skills for the authenticated seeker's resume.
    """
    
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_resume(self):
        """
        Retrieve the authenticated seeker's resume based on the resume_id URL parameter.
        """

        return get_object_or_404(
            Resume,
            pk=self.kwargs["resume_id"],
            user=self.request.user,
        )

    def get_queryset(self):
        """
        Ensure we only operate on skills belonging to the authenticated seeker's resume.
        """

        return Skill.objects.filter(resume=self.get_resume())

    def perform_create(self, serializer):
        """
        Automatically associate the new skill with the authenticated seeker's resume.
        :var serializer: The serializer instance for the skill being created.
        """
        serializer.save(resume=self.get_resume())


class SkillUpdateView(SeekerOnlyMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a skill for the authenticated seeker's resume.
    """

    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensure we only operate on skills belonging to the authenticated seeker's resume.
        """

        return Skill.objects.filter(resume__user=self.request.user)


class LanguageListCreateView(SeekerOnlyMixin, generics.ListCreateAPIView):
    """
    List and create languages for the authenticated seeker's resume.
    """

    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_resume(self):
        """
        Retrieve the authenticated seeker's resume based on the resume_id URL parameter.
        """

        return get_object_or_404(
            Resume,
            pk=self.kwargs["resume_id"],
            user=self.request.user,
        )

    def get_queryset(self):
        """
        Ensure we only operate on languages belonging to the authenticated seeker's resume.
        """

        return Language.objects.filter(resume=self.get_resume())

    def perform_create(self, serializer):
        """
        Automatically associate the new language with the authenticated seeker's resume.
        :var serializer: The serializer instance for the language being created.
        """

        serializer.save(resume=self.get_resume())


class LanguageUpdateView(SeekerOnlyMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a language for the authenticated seeker's resume.
    """
    
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensure we only operate on languages belonging to the authenticated seeker's resume.
        """

        return Language.objects.filter(resume__user=self.request.user)


class ExperienceListCreateView(SeekerOnlyMixin, generics.ListCreateAPIView):
    """
    List and create work experience entries for the authenticated seeker's resume.
    """
    
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_resume(self):
        """
        Retrieve the authenticated seeker's resume based on the resume_id URL parameter.
        """

        return get_object_or_404(
            Resume,
            pk=self.kwargs["resume_id"],
            user=self.request.user,
        )

    def get_queryset(self):
        """
        Ensure we only operate on experience entries belonging to the authenticated seeker's resume.
        """

        return Experience.objects.filter(resume=self.get_resume())

    def perform_create(self, serializer):
        """
        Automatically associate the new experience entry with the authenticated seeker's resume.
        :var serializer: The serializer instance for the experience entry being created.
        """
        
        serializer.save(resume=self.get_resume())


class ExperienceUpdateView(SeekerOnlyMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a work experience entry for the authenticated seeker's resume.
    """
    
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensure we only operate on experience entries belonging to the authenticated seeker's resume.
        """

        return Experience.objects.filter(resume__user=self.request.user)


class EducationListCreateView(SeekerOnlyMixin, generics.ListCreateAPIView):
    """
    List and create education entries for the authenticated seeker's resume.
    """
    
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_resume(self):
        """
        Retrieve the authenticated seeker's resume based on the resume_id URL parameter.
        """

        return get_object_or_404(
            Resume,
            pk=self.kwargs["resume_id"],
            user=self.request.user,
        )

    def get_queryset(self):
        """
        Ensure we only operate on education entries belonging to the authenticated seeker's resume.
        """

        return Education.objects.filter(resume=self.get_resume())

    def perform_create(self, serializer):
        """
        Automatically associate the new education entry with the authenticated seeker's resume.
        :var serializer: The serializer instance for the education entry being created.
        """

        serializer.save(resume=self.get_resume())


class EducationUpdateView(SeekerOnlyMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete an education entry for the authenticated seeker's resume.
    """
    
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensure we only operate on education entries belonging to the authenticated seeker's resume.
        """
        
        return Education.objects.filter(resume__user=self.request.user)