from django.urls import path
from .views import (ConversationListView, ConversationCreateView, ConversationDetailView)

urlpatterns = [
    path("conversations/", ConversationListView.as_view()),
    path("conversations/create/", ConversationCreateView.as_view()),
    path("conversations/<int:pk>/", ConversationDetailView.as_view()),
]