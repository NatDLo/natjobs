"""
Custom permission enforcing seeker-only access where required.
This permission class checks if the authenticated user has a role of 'seeker' to allow access to certain views.
"""

from rest_framework.permissions import BasePermission


class IsSeeker(BasePermission):
    """
    Allows access only to seeker users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'seeker'