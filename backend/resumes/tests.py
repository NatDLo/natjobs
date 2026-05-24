from rest_framework import status
from rest_framework.test import APITestCase

from resumes.models import Resume
from users.models import User


class ResumesApiTests(APITestCase):
    """API tests for seeker-only resume and nested resource management."""

    def create_user(self, username, role, email=None, password="pass12345"):
        if email is None:
            email = f"{username}@example.com"
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
        )

    def resume_payload(self):
        return {
            "full_name": "Ana Perez",
            "location": "Rosario",
            "phone": "123456789",
            "bio": "Python developer",
            "availability": "Full-time",
            "mobility": True,
        }

    def test_seeker_can_create_resume(self):
        """A seeker can create one resume."""
        seeker = self.create_user("seek_resume", "seeker")
        self.client.force_authenticate(user=seeker)

        response = self.client.post("/api/resumes/", self.resume_payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Resume.objects.filter(user=seeker).exists())

    def test_seeker_cannot_create_second_resume(self):
        """A seeker can only have a single resume."""
        seeker = self.create_user("seek_once", "seeker")
        Resume.objects.create(user=seeker, **self.resume_payload())

        self.client.force_authenticate(user=seeker)
        response = self.client.post("/api/resumes/", self.resume_payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recruiter_cannot_access_resume_endpoints(self):
        """Recruiters should be blocked by seeker-only mixin."""
        recruiter = self.create_user("rec_resume", "recruiter")
        self.client.force_authenticate(user=recruiter)

        response = self.client.get("/api/resumes/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seeker_can_add_skill_to_own_resume(self):
        """Seekers should add nested skill records to their own resume."""
        seeker = self.create_user("seek_skill", "seeker")
        resume = Resume.objects.create(user=seeker, **self.resume_payload())

        self.client.force_authenticate(user=seeker)
        response = self.client.post(
            f"/api/resumes/{resume.id}/skills/",
            {"name": "Python", "level": 4},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Python")
        self.assertEqual(response.data["level"], 4)

    def test_seeker_cannot_add_skill_to_other_user_resume(self):
        """Seekers must not access nested resources of another user's resume."""
        owner = self.create_user("owner", "seeker")
        outsider = self.create_user("outsider", "seeker")
        owner_resume = Resume.objects.create(user=owner, **self.resume_payload())

        self.client.force_authenticate(user=outsider)
        response = self.client.post(
            f"/api/resumes/{owner_resume.id}/skills/",
            {"name": "Django", "level": 3},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resume_me_returns_nested_sections(self):
        """Resume me endpoint should include nested arrays such as skills."""
        seeker = self.create_user("seek_me", "seeker")
        resume = Resume.objects.create(user=seeker, **self.resume_payload())

        self.client.force_authenticate(user=seeker)
        self.client.post(
            f"/api/resumes/{resume.id}/skills/",
            {"name": "REST APIs", "level": 4},
            format="json",
        )

        response = self.client.get("/api/resumes/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["skills"]), 1)