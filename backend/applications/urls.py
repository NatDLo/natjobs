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