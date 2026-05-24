from rest_framework import status
from rest_framework.test import APITestCase

from applications.models import Application
from jobs.models import Job
from resumes.models import Resume
from users.models import User


class JobsApiTests(APITestCase):
    """API tests for job listing, creation, and recruiter-side application view."""

    def create_user(self, username, role, email=None, password="pass12345"):
        if email is None:
            email = f"{username}@example.com"
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
        )

    def create_resume_for(self, user):
        return Resume.objects.create(
            user=user,
            full_name=f"{user.username} Name",
            location="Rosario",
            phone="123456789",
            bio="Test bio",
            availability="Full-time",
            mobility=True,
        )

    def test_seeker_sees_only_open_jobs(self):
        """Seekers should only receive open jobs in list endpoint."""
        recruiter = self.create_user("rec_1", "recruiter")
        open_job = Job.objects.create(
            recruiter=recruiter,
            title="Frontend Dev",
            description="Angular role",
            location="Rosario",
            status="open",
        )
        Job.objects.create(
            recruiter=recruiter,
            title="Closed Position",
            description="No longer available",
            location="CABA",
            status="closed",
        )

        seeker = self.create_user("seek_1", "seeker")
        self.client.force_authenticate(user=seeker)
        response = self.client.get("/api/jobs/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], open_job.id)

    def test_recruiter_sees_only_own_jobs(self):
        """Recruiters should list only jobs they own."""
        recruiter_a = self.create_user("rec_a", "recruiter")
        recruiter_b = self.create_user("rec_b", "recruiter")
        own_job = Job.objects.create(
            recruiter=recruiter_a,
            title="Backend Dev",
            description="Django role",
            location="Cordoba",
            status="open",
        )
        Job.objects.create(
            recruiter=recruiter_b,
            title="Other Recruiter Job",
            description="Different owner",
            location="Mendoza",
            status="open",
        )

        self.client.force_authenticate(user=recruiter_a)
        response = self.client.get("/api/jobs/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], own_job.id)

    def test_seeker_cannot_create_job(self):
        """Only recruiters should be able to create jobs."""
        seeker = self.create_user("seek_create", "seeker")
        self.client.force_authenticate(user=seeker)

        payload = {
            "title": "Should Fail",
            "description": "Seeker cannot create this",
            "location": "Rosario",
            "status": "open",
        }
        response = self.client.post("/api/jobs/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_recruiter_can_create_job(self):
        """Recruiters can create jobs and owner should be set automatically."""
        recruiter = self.create_user("rec_create", "recruiter")
        self.client.force_authenticate(user=recruiter)

        payload = {
            "title": "Python Developer",
            "description": "Build APIs",
            "location": "Remote",
            "status": "open",
        }
        response = self.client.post("/api/jobs/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        job = Job.objects.get(id=response.data["id"])
        self.assertEqual(job.recruiter_id, recruiter.id)

    def test_recruiter_can_view_applications_for_own_job(self):
        """Recruiter should list applications attached to their own job."""
        recruiter = self.create_user("rec_apps", "recruiter")
        seeker = self.create_user("seek_apps", "seeker")
        resume = self.create_resume_for(seeker)

        job = Job.objects.create(
            recruiter=recruiter,
            title="QA Engineer",
            description="Testing role",
            location="Rosario",
            status="open",
        )
        Application.objects.create(
            seeker=seeker,
            job=job,
            resume=resume,
            status="applied",
            notes="Ready to start",
        )

        self.client.force_authenticate(user=recruiter)
        response = self.client.get(f"/api/jobs/{job.id}/applications/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["job"]["id"], job.id)