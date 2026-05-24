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
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return User.objects.select_related(
            "seekerprofile",
            "recruiterprofile",
        ).get(pk=self.request.user.pk)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UserMeSerializer
        return UserMeUpdateSerializer

    def update(self, request, *args, **kwargs):
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
    serializer_class = UserPublicProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = User.objects.select_related(
        "seekerprofile",
        "recruiterprofile",
    )