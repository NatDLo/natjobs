from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import RecruiterProfile, SeekerProfile, User


class UsersApiTests(APITestCase):
    """API tests for registration, profile retrieval, and profile updates."""

    def create_user(self, username, role, email=None, password="pass12345"):
        if email is None:
            email = f"{username}@example.com"
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
        )

    def test_register_creates_user_and_role_profile(self):
        """Register endpoint should create a user and auto-create seeker profile via signal."""
        payload = {
            "username": "ana",
            "email": "ana@example.com",
            "password": "strongpass123",
            "first_name": "Ana",
            "last_name": "Diaz",
            "role": "seeker",
        }

        response = self.client.post("/api/users/register/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="ana")
        self.assertEqual(user.role, "seeker")
        self.assertTrue(SeekerProfile.objects.filter(user=user).exists())

    def test_me_returns_authenticated_user_profile(self):
        """Authenticated user should retrieve own profile including nested recruiter data."""
        recruiter = self.create_user("recruiter_1", "recruiter")
        RecruiterProfile.objects.filter(user=recruiter).update(company_name="ACME Inc")

        self.client.force_authenticate(user=recruiter)
        response = self.client.get("/api/users/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], recruiter.id)
        self.assertEqual(response.data["role"], "recruiter")
        self.assertEqual(response.data["recruiter_profile"]["company_name"], "ACME Inc")

    def test_seeker_cannot_update_company_name(self):
        """Seekers cannot update recruiter-only field company_name."""
        seeker = self.create_user("seeker_1", "seeker")

        self.client.force_authenticate(user=seeker)
        response = self.client.patch(
            "/api/users/me/",
            {"company_name": "Should Fail"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("company_name", response.data)

    def test_recruiter_can_update_company_name(self):
        """Recruiters should be able to update company_name through me endpoint."""
        recruiter = self.create_user("recruiter_2", "recruiter")

        self.client.force_authenticate(user=recruiter)
        response = self.client.patch(
            "/api/users/me/",
            {"company_name": "New Company"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recruiter.refresh_from_db()
        profile = RecruiterProfile.objects.get(user=recruiter)
        self.assertEqual(profile.company_name, "New Company")

    def test_public_profile_is_retrievable_for_authenticated_user(self):
        """Authenticated users should be able to retrieve another user's public profile."""
        target = self.create_user("target_user", "seeker")
        viewer = self.create_user("viewer_user", "recruiter")

        self.client.force_authenticate(user=viewer)
        response = self.client.get(f"/api/users/{target.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], target.id)

    def test_backfill_command_creates_missing_profiles(self):
        """Backfill command should restore missing role-specific profiles."""
        seeker = self.create_user("missing_seek", "seeker")
        recruiter = self.create_user("missing_rec", "recruiter")

        SeekerProfile.objects.filter(user=seeker).delete()
        RecruiterProfile.objects.filter(user=recruiter).delete()

        call_command("backfill_user_profiles")

        self.assertTrue(SeekerProfile.objects.filter(user=seeker).exists())
        self.assertTrue(RecruiterProfile.objects.filter(user=recruiter).exists())