from rest_framework import status
from rest_framework.test import APITestCase

from applications.models import Application
from jobs.models import Job
from resumes.models import Resume
from users.models import User


class ApplicationsApiTests(APITestCase):
    """API tests for seeker applications and recruiter status management."""

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
            bio="Seeker profile",
            availability="Full-time",
            mobility=True,
        )

    def create_job_for(self, recruiter, status_value="open"):
        return Job.objects.create(
            recruiter=recruiter,
            title="Backend Engineer",
            description="Build Django APIs",
            location="Remote",
            status=status_value,
        )

    def test_seeker_can_apply_to_open_job(self):
        """Seeker with resume can create an application to an open job."""
        recruiter = self.create_user("rec_apply", "recruiter")
        seeker = self.create_user("seek_apply", "seeker")
        self.create_resume_for(seeker)
        job = self.create_job_for(recruiter, "open")

        self.client.force_authenticate(user=seeker)
        response = self.client.post(
            "/api/applications/",
            {"job_id": job.id, "notes": "Interested in this role"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        app = Application.objects.first()
        self.assertEqual(app.seeker_id, seeker.id)
        self.assertEqual(app.job_id, job.id)

    def test_duplicate_application_is_blocked(self):
        """Same seeker should not be able to apply twice to the same job."""
        recruiter = self.create_user("rec_dup", "recruiter")
        seeker = self.create_user("seek_dup", "seeker")
        self.create_resume_for(seeker)
        job = self.create_job_for(recruiter, "open")

        self.client.force_authenticate(user=seeker)
        self.client.post("/api/applications/", {"job_id": job.id}, format="json")
        response = self.client.post("/api/applications/", {"job_id": job.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_application_requires_existing_resume(self):
        """Seeker must create resume before applying."""
        recruiter = self.create_user("rec_no_resume", "recruiter")
        seeker = self.create_user("seek_no_resume", "seeker")
        job = self.create_job_for(recruiter, "open")

        self.client.force_authenticate(user=seeker)
        response = self.client.post("/api/applications/", {"job_id": job.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_apply_to_non_open_job(self):
        """Applications should fail when job is not open."""
        recruiter = self.create_user("rec_closed", "recruiter")
        seeker = self.create_user("seek_closed", "seeker")
        self.create_resume_for(seeker)
        job = self.create_job_for(recruiter, "closed")

        self.client.force_authenticate(user=seeker)
        response = self.client.post("/api/applications/", {"job_id": job.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recruiter_can_update_status_for_own_job_application(self):
        """Recruiter owner can move application through status pipeline."""
        recruiter = self.create_user("rec_owner", "recruiter")
        seeker = self.create_user("seek_owner", "seeker")
        resume = self.create_resume_for(seeker)
        job = self.create_job_for(recruiter, "open")
        application = Application.objects.create(
            seeker=seeker,
            job=job,
            resume=resume,
            status="applied",
            notes="Initial note",
        )

        self.client.force_authenticate(user=recruiter)
        response = self.client.patch(
            f"/api/applications/{application.id}/status/",
            {"status": "reviewing", "notes": "Screening"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        application.refresh_from_db()
        self.assertEqual(application.status, "reviewing")
        self.assertEqual(application.notes, "Screening")

    def test_recruiter_cannot_update_status_for_other_recruiter_job(self):
        """Recruiter should not update applications of jobs they do not own."""
        owner = self.create_user("owner_rec", "recruiter")
        other = self.create_user("other_rec", "recruiter")
        seeker = self.create_user("seek_other", "seeker")
        resume = self.create_resume_for(seeker)
        job = self.create_job_for(owner, "open")
        application = Application.objects.create(seeker=seeker, job=job, resume=resume)

        self.client.force_authenticate(user=other)
        response = self.client.patch(
            f"/api/applications/{application.id}/status/",
            {"status": "rejected"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)