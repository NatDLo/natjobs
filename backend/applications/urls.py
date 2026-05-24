"""
URL routes for applications and recruiter-side status updates.
Defines endpoints for seekers to create and view their applications, and for recruiters to update application status.
"""

from django.urls import path
from .views import (
    ApplicationListCreateView,
    ApplicationDetailView,
    ApplicationUpdateStatusView,
)

urlpatterns = [
    path("", ApplicationListCreateView.as_view()),
    path("<int:pk>/", ApplicationDetailView.as_view()),
    path("<int:pk>/status/", ApplicationUpdateStatusView.as_view()),
]