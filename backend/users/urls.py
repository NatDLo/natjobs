from django.urls import path
from .views import MeView, RegisterView, UserPublicProfileView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("<int:pk>/", UserPublicProfileView.as_view(), name="user-public-profile"),
]