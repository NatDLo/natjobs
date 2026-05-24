"""
HTTP URL routes for conversation resources.
Only authenticated users can access these endpoints, and they can only see conversations they are a part of.
"""

from django.urls import path
from .views import (ConversationListView, ConversationCreateView, ConversationDetailView)

urlpatterns = [
    path("conversations/", ConversationListView.as_view()),
    path("conversations/create/", ConversationCreateView.as_view()),
    path("conversations/<int:pk>/", ConversationDetailView.as_view()),
]