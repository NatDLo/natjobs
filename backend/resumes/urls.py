from django.urls import path
from .views import (
    ResumeListCreateView,
    ResumeMeView,
    ResumeDetailView,
    SkillListCreateView,
    SkillUpdateView,
    LanguageListCreateView,
    LanguageUpdateView,
    ExperienceListCreateView,
    ExperienceUpdateView,
    EducationListCreateView,
    EducationUpdateView,
)

urlpatterns = [
    path("", ResumeListCreateView.as_view()),
    path("me/", ResumeMeView.as_view()),
    path("<int:pk>/", ResumeDetailView.as_view()),

    path("<int:resume_id>/skills/", SkillListCreateView.as_view()),
    path("skills/<int:pk>/", SkillUpdateView.as_view()),

    path("<int:resume_id>/languages/", LanguageListCreateView.as_view()),
    path("languages/<int:pk>/", LanguageUpdateView.as_view()),

    path("<int:resume_id>/experiences/", ExperienceListCreateView.as_view()),
    path("experiences/<int:pk>/", ExperienceUpdateView.as_view()),

    path("<int:resume_id>/education/", EducationListCreateView.as_view()),
    path("education/<int:pk>/", EducationUpdateView.as_view()),
]