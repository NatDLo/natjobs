"""
Views for user management, including registration, profile retrieval, and profile updates.
"""

from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import User
from .serializers import (
    UserMeSerializer,
    UserMeUpdateSerializer,
    UserPublicProfileSerializer,
    UserRegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    """
    View to register a new user.
    POST: Create a new user account.
    """

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class MeView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve and update the authenticated user's profile.
    GET: Retrieve the authenticated user's profile.
    PUT/PATCH: Update the authenticated user's profile.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Return the authenticated user's profile.
        """

        return User.objects.select_related(
            "seekerprofile",
            "recruiterprofile",
        ).get(pk=self.request.user.pk)

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the request method.
        - For GET requests, use UserMeSerializer to retrieve the user's profile.
        - For PUT/PATCH requests, use UserMeUpdateSerializer to update the user's profile.
        """

        if self.request.method in permissions.SAFE_METHODS:
            return UserMeSerializer
        return UserMeUpdateSerializer

    def update(self, request, *args, **kwargs):
        """
        Override the update method to return the updated user profile after a successful update.
        """

        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance.refresh_from_db()

        response_serializer = UserMeSerializer(
            instance,
            context=self.get_serializer_context(),
        )
        return Response(response_serializer.data)


class UserPublicProfileView(generics.RetrieveAPIView):
    """
    View to retrieve a user's public profile.
    GET: Retrieve a user's public profile by their ID.
    """
    
    serializer_class = UserPublicProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = User.objects.select_related(
        "seekerprofile",
        "recruiterprofile",
    )