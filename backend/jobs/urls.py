"""
URL routes for job listing, detail, updates, and recruiter-side applications view.
"""

from django.urls import path
from .views import JobListCreateView, JobDetailView, JobUpdateView, JobApplicationsView

urlpatterns = [
    path('', JobListCreateView.as_view()),
    path('<int:pk>/', JobDetailView.as_view()),
    path('<int:pk>/update/', JobUpdateView.as_view()),
    path('<int:job_id>/applications/', JobApplicationsView.as_view()),
]